import pandas as pd
import numpy as np


def get_control_peptide(melted_df: pd.DataFrame) -> str:
    """
    Identify the control peptide with the highest score to serve as a control
    against which to compare relative abundances

    Parameters:
    melted_df (DataFrame): Data with 'Precursor.Id' and 'Abundance' columns.
    include_cysteine (bool), default=False: If true, control peptides are 
        allowed to contain cysteine

    Returns:
    str: The peptide ID with the highest Z-score, excluding cysteine peptides.

        * Reutrns None if no suitable control peptides are found. *
    """
    # Check if there are suitable control peptide candidates
    candidate_peptides = [
        pep for pep in melted_df["Precursor.Id"].unique() if "C" not in pep
    ]
    if len(candidate_peptides) == 0:
        return None
    # If there's only one possible control peptide, we'll just use it
    elif len(candidate_peptides) == 1: 
        return candidate_peptides[0]

    # Calculate mean and standard deviation for each candidate control peptide
    candidate_df = melted_df[
        melted_df["Precursor.Id"].isin(candidate_peptides)
    ].copy()
    agg_df = (
        candidate_df.groupby("Precursor.Id", observed=False)["Abundance"]
        .agg(["mean", "std"])
        .reset_index()
    )

    # Calculate score
    overall_mean = agg_df["mean"].mean()
    agg_df["score"] = (agg_df["mean"] - overall_mean) / agg_df["std"]

    # Get the peptide with the highest score
    control_peptide = agg_df.loc[
        agg_df["score"] == agg_df["score"].max(), "Precursor.Id"
    ].iloc[0]
    
    return control_peptide

def contains_cysteine_peptides(df) -> bool:
    """Check if the DataFrame contains cysteine peptides.

    Args:
        df pd.DataFrame: A dataframe with a 'Precursor.Id' column. 

    Returns:
        bool: True if there are cysteine peptides, False otherwise.
    """
    cysteine_peptides = [ 
        pep for pep in df["Precursor.Id"].unique() if "C" in pep
    ]
    return len(cysteine_peptides) > 0



def subset_dataframe(
        melted_df: pd.DataFrame, control_peptide: str
        ) -> pd.DataFrame:
    """
    Subset the DataFrame to only include specified precursors.

    Parameters:
    melted_df (pd.DataFrame): DataFrame containing 'Precursor.Id', 'Abundance',
                              and 'Compound' columns.
    precursors (List[str]): List of precursor IDs to subset by.

    Returns:
    pd.DataFrame: Subsetted DataFrame with only specified precursors.
    """
    cys_peptides = [
        pep for pep in melted_df["Precursor.Id"].unique() if "C" in pep
    ]

    # Subset for control and cysteine peptides
    df = df[df['Precursor.Id'].isin([control_peptide] + cys_peptides)]
    
    return df

def scale_abundance(df: pd.DataFrame) -> pd.DataFrame:
    """Create a new column with scaled abundance values for each precursor 
    using the scale_series function.

    Args:
        df (pd.DataFrame): A dataframe with 'Precursor.Id' and 'Abundance'
            columns containg cysteine and control peptides.

    Returns:
        pd.DataFrame: The input dataframe with a new 'scaled_abundance' column.
    """
    df["scaled_abundance"] = (
        df.groupby("Precursor.Id", observed=False)["Abundance"]
        .transform(scale_series)
    )
    return df

def scale_series(series: pd.Series) -> pd.Series:
    """
    Scale a series to a specified range with a target mean.

    Parameters:
    series (pd.Series): Series to scale.

    Returns:
    pd.Series: Scaled series with values in the specified range.
    """
    new_min = 0.0
    new_mean = 0.5
    new_max = 1

    # Normalize series to [0, 1]
    normalized = (series - series.min()) / (series.max() - series.min())

    # Calculate scaling factor to adjust the mean
    scaling_factor = (new_mean - new_min) / normalized.mean()
    scaled = normalized * scaling_factor

    # Adjust to new min and max
    scaled = scaled * (new_max - new_min) + new_min

    # Replace infinities with NaN
    scaled = scaled.replace([np.inf, -np.inf], np.nan)

    return scaled

def normalize_to_control(
        df: pd.DataFrame, control_peptide: str) -> pd.DataFrame:
    """Normalize the scaled abundance values to the control peptide by dividing
    the scaled abundance values by the control peptide abundance values for each
    compound by filename. If there is a filename where the control peptide is 
    NaN, the control peptide abundance will be the mean of the other control
    peptide values for that compound.

    Args:
        df (pd.DataFrame): A dataframe containing scaled abundance values for 
            the cysteine and control peptides and columns Filename and Compound.
        control_peptide (str): The control peptide chosen previously.

    Returns:
        pd.DataFrame: The same dataframe with the scaled abundance values 
            normalized to the control peptide.
    """
    # Extract control values per Filename
    control_values = (
        df[df["Precursor.Id"] == control_peptide]
        .set_index("Filename")[["scaled_abundance", "Compound"]]
        .rename(columns={"scaled_abundance": "control_value"})
    )

    # Merge control values back into the original dataframe
    df = df.merge(control_values, on=["Filename", "Compound"], how="left")

    # Fill NaN control values with the mean within the same Compound
    # If the control peptide is not present for any replicates of the compound,
    # keep the NaN values
    compound_means = control_values.groupby("Compound")["control_value"].mean()
    df["control_value"] = df["control_value"].fillna(
        df["Compound"].map(compound_means)
    )

    # Normalize scaled abundance values to the control peptide
    df["relative_abundance"] = df["scaled_abundance"] / df["control_value"]

    # Drop intermediate control_value column
    df.drop(columns=["control_value"], inplace=True)

    # Remove the control peptide from the dataframe
    df = df[df["Precursor.Id"] != control_peptide]

    return df

def get_relative_abundance(melted_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate relative abundance for a single gene by normalizing peptide data.

    Parameters:
    melted_df (pd.DataFrame): DataFrame with (at least) the columns: 
        'Genes', 'Precursor.Id', 'Abundance', and 'Compound' 

    Returns:
    pd.DataFrame: DataFrame with relative abundances normalized to a control
                  peptide, with the maximum compound row removed.
                  
                  *If there are no cysteine peptides or no adequate control
                  peptides are found, returns an empty DataFrame.* 
    
    Raises:
    ValueError: If more than one unique gene is found in the DataFrame.
    """
    # Ensure only one gene is present
    if melted_df["Genes"].nunique() > 1:
        raise ValueError("Relative abundance can only be calculated for one "
                         "gene at a time.")
    
    # Check if there are cysteine peptides, return empty DataFrame if not
    if not contains_cysteine_peptides(melted_df):
        return pd.DataFrame()
    
    # Identify control precursor, return empty DataFrame if none found
    control_precursor = get_control_peptide(melted_df)
    if control_precursor is None:
        return pd.DataFrame()
    
    # Get list of all precursors, control and cysteine
    cysteine_precursor = [
        pep for pep in melted_df["Precursor.Id"].unique() if "C" in pep
    ]
    precursor_list = cysteine_precursor + [control_precursor]

    # Subset, scale, and normalize data
    subset_df = subset_dataframe(melted_df, precursor_list)
    scaled_df = scale_abundance(subset_df)
    normalized_df = normalize_to_control(scaled_df, control_precursor)

    return normalized_df

