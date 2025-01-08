import asyncio
from typing import Union
import pandas as pd
from collections.abc import Callable
from rapidfuzz import process, fuzz
from ..exceptions import ComponentError, ConfigError
from .tPandas import tPandas
from ..interfaces.databases import DBSupport

def preprocess_address(address):
    """Preprocess Address for Fuzzy String Matching.
    """
    if pd.isnull(address):
        return ""
    # Convert to lowercase, remove punctuation, and strip whitespace
    address = address.replace('.', '').strip()
    return address


class PlacerStores(DBSupport, tPandas):
    """
        PlacerStores.

        Overview

        The `PlacerStores` is used to match PlacerAI stores with Stores tables at different schemas.

        Properties

        .. table:: Properties
        :widths: auto

        +------------------+----------+-----------+-----------------------------------------------------------------------------------+
        | Name             | Required | Type      | Description                                                                       |
        +------------------+----------+-----------+-----------------------------------------------------------------------------------+
        | location_field   | Yes      | str       | The name of the column to be used for matching.                                   |
        +------------------+----------+-----------+-----------------------------------------------------------------------------------+

        Return
           A New Dataframe with all stores matching using a Fuzzy Search Match.

    """  # noqa

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self._column: Union[str, list] = kwargs.pop("location_field", None)
        self._account: str = kwargs.pop("account_field", 'program_slug')
        if not self._column:
            raise ConfigError(
                "PlacerStores requires a column for matching => **location_field**"
            )
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    def find_best_match(self, address, choices, threshold: int = 80, token_threshold: int = 80):
        """
        Find the best fuzzy match for a given address.

        Parameters:
        - address (str): The address to match.
        - choices (list): List of addresses to match against.
        - threshold (int): Minimum similarity score to consider a match.

        Returns:
        - best_match (str) or None: The best matching address or None if no match meets the threshold.
        - score (int): The similarity score of the best match.
        """
        match = process.extractOne(address, choices, scorer=fuzz.token_sort_ratio)
        if match and match[1] >= threshold:
            return match[0], match[1]

        # evaluate if all tokens (words) are matching on different order:
        match = process.extractOne(address, choices, scorer=fuzz.token_set_ratio)
        if match and match[1] >= token_threshold:
            return match[0], match[1]

        # still not match, return None
        return None, None

    def match_addresses(self, data_row, store_addresses, df_stores):
        best_match, score = self.find_best_match(
            data_row[self._column], store_addresses, threshold=80)
        if best_match:
            matched_store = df_stores[df_stores[self._column] == best_match].iloc[0]
            return pd.Series({
                'store_id': matched_store['store_id'],
                'place_id': matched_store['place_id'],
                'matched_formatted_address': matched_store[self._column],
                'similarity_score': score
            })
        else:
            return pd.Series({
                'store_id': None,
                'place_id': None,
                'matched_formatted_address': None,
                'similarity_score': score
            })

    async def _run(self):
        try:
            # Create a Group By program_slug to extract the retailers:
            retailers = self.data[self._account].drop_duplicates().reset_index(drop=True)
            # Preprocess addresses for primary stores:
            self.data[self._column] = self.data[self._column].apply(preprocess_address)
            # Iterate over every retailer and query the list of stores for that particular program:
            db = self.default_connection('pg')
            for retailer in retailers.values:
                self._logger.notice(f' Evaluating Program {retailer} ...')
                query = f"select store_id, place_id, formatted_address from {retailer}.stores"
                async with await db.connection() as conn:
                    try:
                        result = await conn.fetchall(query)
                    except Exception as e:
                        self._logger.error(f'Error Matching Query: {e}')
                        continue
                    df_stores = pd.DataFrame([dict(store) for store in result])
                    # check first if df_stores is empty
                    if df_stores.empty:
                        self._logger.warning(f'No Stores Found for Program {retailer}')
                        continue
                    # Preprocess addresses for secondary stores:
                    df_stores[self._column] = df_stores[self._column].apply(preprocess_address)
                    # convert all store addresses to a list:
                    store_addresses = df_stores[self._column].tolist()
                    # filter the store data to retailer:
                    df_data = self.data[self.data[self._account] == retailer].copy()
                    matched_df = df_data.apply(
                        self.match_addresses,
                        axis=1,
                        store_addresses=store_addresses,
                        df_stores=df_stores
                    )
                    print('Matched : ', matched_df.head())
                    self.data = self.data.join(matched_df, how='left', rsuffix='_matched')
            # Remove the temporary columns:
            try:
                self.data = self.data.drop(
                    columns=[f'matched_{self._column}', 'similarity_score']
                )
            except KeyError:
                pass  # The columns might not exist if no matches were found.
            return self.data

        except Exception as err:
            raise ComponentError(
                f"Generic Error on Data: error: {err}"
            ) from err
