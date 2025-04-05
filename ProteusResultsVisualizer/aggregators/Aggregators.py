from abc import ABC, abstractmethod
from typing import Any


class Aggregator(ABC):
    @abstractmethod
    def aggregate(self, df: Any) -> Any:
        """
        Aggregates the given DataFrame and returns a new aggregated DataFrame.
        The input DataFrame can be either a pandas DataFrame or a polars DataFrame.
        """
        pass


class ComponentWiseExtremaAggregator(Aggregator):
    def aggregate(self, df: Any) -> Any:
        """
        Computes component-wise extrema (max and min) for each column.
        This implementation assumes df supports .max() and .min() methods.
        For pandas, these methods return a Series.
        """
        try:
            # For pandas, compute max and min per column.
            max_vals = df.max()
            min_vals = df.min()

            # Here we're assuming a pandas DataFrame output.
            # You might need to check the type of df to support polars.
            import pandas as pd
            max_df = pd.DataFrame(max_vals).T.rename(index={0: "Max"})
            min_df = pd.DataFrame(min_vals).T.rename(index={0: "Min"})
            aggregated_df = pd.concat([max_df, min_df])
            return aggregated_df
        except Exception as e:
            raise NotImplementedError(f"Aggregation for this DataFrame type is not implemented yet: {e}")


class MeanAggregator(Aggregator):
    def aggregate(self, df: Any) -> Any:
        """
        Computes the mean of each column.
        """
        try:
            mean_vals = df.mean()
            import pandas as pd
            mean_df = pd.DataFrame(mean_vals).T.rename(index={0: "Mean"})
            return mean_df
        except Exception as e:
            raise NotImplementedError(f"Aggregation for this DataFrame type is not implemented yet: {e}")


def perform_aggregation(df: Any, aggregator: Aggregator) -> Any:
    return aggregator.aggregate(df)


