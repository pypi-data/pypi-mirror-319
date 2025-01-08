import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from epidemic_intelligence.templates import netsi
from epidemic_intelligence.helper import execute, build_geographic_filter, build_categorical_filter

def build_ap_query(table_name: str, reference_table: str, source_geo_level: str, 
                   target_geo_level: str, output_resolution: str = None, 
                   source_values=None, target_values=None, 
                   source_column='source_basin', target_column='target_basin', reference_column='basin_id',
                    
                   cutoff: float = 0.05, display: str = "source", value: str = "importations", 
                   domestic: bool = True) -> str:
    """Builds an SQL query for analyzing importation data with an area plot.
    Inputs:
        table_name (str): BigQuery table name in "dataset.table" format containing importation data
        reference_table (str): BigQuery table name in "dataset.table" format containing GLEAM or LEAM-US geography mappings
        source_geo_level (str): a column in reference_table used to slice data by source, eg `region_label`
        target_geo_level (str): a column in reference_table used to slice data by target, eg `region_label`
        output_resolution (str): a column in reference_table, geographic resolution of resulting graph. defaults to target_geo_level
        source_values (list or str): values of source_geo_level that will be included as source nodes, eg `Northern Europe`. set to None to include all. 
        target_values (list or str): values of target_geo_level that will be included as target nodes, eg `Northern Europe`. set to None to include all. 
        domestic (bool): whether or not cases originating and ending in target_values will be included
        cutoff (float): any geography contributing under the cutoff (between 0 and 1) will be aggregated into `Other`, defaults to 0.05
        display (str): "source" or "target", whether imports to targets or exports from sources will be displayed, defaults to "source"
        date (str): time series aggregation method, "day" for by day, "iso" for by ISO week. 
    
    Returns
        query (str): formatted BigQuery query
    """

    source_filter = build_geographic_filter(source_geo_level, source_values, alias="g_source") if source_values is not None else "TRUE"
    target_filter = build_geographic_filter(target_geo_level, target_values, alias="g_target") if target_values is not None else  "TRUE"
    
    where_clauses = [target_filter, source_filter]
    
    if not domestic:
        where_clauses.append(f"g_source.{output_resolution} <> g_target.{output_resolution}")

    where_clause = " AND ".join(where_clauses)

    query = f"""
    WITH region_imports AS (
    SELECT
        g_{display}.{output_resolution} AS {display}_label, 
       SUM({value}) AS importations
    FROM 
        `{table_name}` AS i
    JOIN 
        `{reference_table}` AS g_source 
        ON g_source.{reference_column} = i.{source_column}
    JOIN 
        `{reference_table}` AS g_target 
        ON g_target.{reference_column} = i.{target_column}
    WHERE 
        {where_clause}
    GROUP BY
        g_{display}.{output_resolution}
    ), 
    total_imports AS (
      SELECT 
        SUM(importations) AS grand_total_importations 
      FROM region_imports
    ),
    categorized_regions AS (
      SELECT 
        r.{display}_label,
        CASE 
          WHEN r.importations < ({cutoff} * (SELECT grand_total_importations FROM total_imports)) THEN "Other"
          ELSE r.{display}_label
        END AS categorized_label
      FROM 
        region_imports r
    )
    SELECT 
      cr.categorized_label AS {display}, 
      i.date AS date, 
      SUM(i.importations) AS importations,
    FROM 
      `{table_name}` AS i
    JOIN 
      `{reference_table}` AS g_target 
      ON g_target.{reference_column} = i.{target_column}
    JOIN 
      `{reference_table}` AS g_source 
      ON g_source.{reference_column} = i.{source_column}
    JOIN 
      categorized_regions cr 
      ON cr.{display}_label = g_{display}.{output_resolution}
    WHERE 
      {where_clause}
    GROUP BY 
      cr.categorized_label, 
      i.date
    ORDER BY 
      i.date;
    """
    return query

def create_area_plot(data: pd.DataFrame, value: str, title: str = "Area Plot", 
                     xlabel: str = "Date", ylabel: str = "Exportations", 
                     legendlabel: str = "Source", display: str = "source") -> go.Figure:
    """Creates an area plot using the provided data."""
    fig = px.area(data, x="date", y=value, color=display, template=netsi)
    fig.update_traces(line=dict(width=0.4))
    fig.update_layout(title_text=title, legend_traceorder="reversed",
                      xaxis_title=xlabel, yaxis_title=ylabel, legend_title_text=legendlabel)
    return fig

def area_plot(client, table_name: str, reference_table: str,
                                 source_geo_level: str, target_geo_level: str,
                                 output_resolution: str = None, 
                                 source_values=None, target_values=None, 
                                 source_column='source_basin', target_column='target_basin', reference_column='basin_id',
                                 domestic: bool = True, cutoff: float = 0.05,
                                 value: str = "importations", 
                                 display: str = "source") -> go.Figure:
    """Creates an area plot by executing a query based on the provided parameters.
    
    Inputs:
        client (google.cloud.bigquery.Client): initialized BigQuery client
        table_name (str): BigQuery table name in "dataset.table" format containing importation data
        reference_table (str): BigQuery table name in "dataset.table" format containing GLEAM or LEAM-US geography mappings
        source_geo_level (str): a column in reference_table used to slice data by source, eg `region_label`
        target_geo_level (str): a column in reference_table used to slice data by target, eg `region_label`
        output_resolution (str): a column in reference_table, geographic resolution of resulting graph. defaults to target_geo_level
        source_values (list or str): values of source_geo_level that will be included as source nodes, eg `Northern Europe`. set to None to include all. 
        target_values (list or str): values of target_geo_level that will be included as target nodes, eg `Northern Europe`. set to None to include all. 
        domestic (bool): whether or not cases originating and ending in target_values will be included
        cutoff (float): any geography contributing under the cutoff (between 0 and 1) will be aggregated into `Other`, defaults to 0.05
        display (str): "source" or "target", whether imports to targets or exports from sources will be displayed, defaults to "source"
        
    Returns:
        fig (plotly.graph_objects.Figure): formatted area plot
    """
    
    # Step 1: Build the query
    query = build_ap_query(
        table_name=table_name,
        reference_table=reference_table,
        source_geo_level=source_geo_level,
        target_geo_level=target_geo_level,
        output_resolution=output_resolution,
        source_values=source_values,
        target_values=target_values,
        domestic=domestic,
        cutoff=cutoff,
        display=display,
        value=value,
        source_column=source_column, 
        target_column=target_column, 
        reference_column=reference_column,
    )
    
    # Step 2: Execute the query
    data = execute(client, query)
    
    # Step 3: Create the area plot
    fig = create_area_plot(data, value=value,  
                           xlabel="Date", ylabel="Exportations" if display=="source" else "Importations", 
                           legendlabel=display.capitalize(), display=display)
    
    return fig

def fetch_area_plot_data(fig):
    df = pd.DataFrame()
    for trace in fig.data:
        dct = pd.DataFrame({trace.legendgroup: trace.y}, index=trace.x)
        df = pd.concat([df, dct], axis=1)

    df = pd.melt(df, 
        var_name = fig.layout.legend.title.text.lower(),
        value_name = fig.layout.yaxis.title.text.lower(),
        ignore_index = False
       )

    return df


def build_sankey_query(table_name, reference_table, source_geo_level, target_geo_level, source_values, target_values, 
                       date_range, value='importations', 
                       source_col='source_basin', target_col='target_basin', reference_col='basin_id',
                       cutoff=0.05, source_resolution=None, target_resolution=None, domestic=True,
                       n_sources=100, n_targets=100,
                       categories=None, category_col='category'):
                       
    if source_resolution == None:
        source_resolution = source_geo_level
    if target_resolution == None:
        target_resolution = target_geo_level

    # i dont know why this is needed but apparently it is
    if n_sources==None:
        n_sources = 100
    if n_targets==None:
        n_targets = 100
                       
    # Build filters for both source and target regions
    source_filter = build_geographic_filter(source_geo_level, source_values, alias="g_source")
    target_filter = build_geographic_filter(target_geo_level, target_values, alias="g_target")
    # cat_filter = build_categorical_filter(categories, category_col=category_col) if categories is not None else "TRUE"
    
    # Create the base where clause
    where_clauses = []

    if source_filter:
        where_clauses.append(source_filter)
    if target_filter:
        where_clauses.append(target_filter)
    # if cat_filter:
    #     where_clauses.append(cat_filter)
        
    if not domestic:
        # Exclude rows where target imports to itself
        where_clauses.append(f"g_source.{target_resolution} != g_target.{target_resolution}")

    # Join the where clauses with "AND"
    where_clause = " AND ".join(where_clauses)

    query = f"""
    WITH total_exportations AS (
        -- Calculate total exportations for the given date range
        SELECT 
            SUM(i.{value}) AS total_sum
        FROM 
            `{table_name}` AS i
        JOIN 
            `{reference_table}` AS g_target 
            ON g_target.{reference_col} = i.{target_col}
        JOIN 
            `{reference_table}` AS g_source 
            ON g_source.{reference_col} = i.{source_col}
        WHERE 
            {where_clause}
            AND i.date >= "{date_range[0]}"
            AND i.date <= "{date_range[1]}"
    ), source_totals AS (
        -- Calculate total exportations for each source
        SELECT
            g_source.{source_resolution.split("_")[0]+"_id"} * -1 AS sourceid,
            g_source.{source_resolution} AS source,
            SUM(i.importations) AS source_sum
        FROM 
            `{table_name}` AS i
        JOIN 
            `{reference_table}` AS g_target 
            ON g_target.{reference_col} = i.{target_col}
        JOIN 
            `{reference_table}` AS g_source 
            ON g_source.{reference_col} = i.{source_col}
        WHERE 
            {where_clause}
            AND i.date >= "{date_range[0]}"
            AND i.date <= "{date_range[1]}"
        GROUP BY sourceid, source
    ), target_totals AS (
        -- Calculate total exportations for each target
        SELECT
            g_target.{target_resolution.split("_")[0]+"_id"} AS targetid,
            g_target.{target_resolution} AS target,
            SUM(i.importations) AS target_sum
            
        FROM 
            `{table_name}` AS i
        JOIN 
            `{reference_table}` AS g_target 
            ON g_target.{reference_col} = i.{target_col}
        JOIN 
            `{reference_table}` AS g_source 
            ON g_source.{reference_col} = i.{source_col}
        WHERE 
            {where_clause}
            AND i.date >= "{date_range[0]}"
            AND i.date <= "{date_range[1]}"
        GROUP BY targetid, target
    ), ranked_targets AS (
        -- Rank targets based on their target_sum
        SELECT 
            tt.targetid,
            tt.target,
            tt.target_sum,
            ROW_NUMBER() OVER (ORDER BY tt.target_sum DESC) AS rank
        FROM 
            target_totals tt
    ), ranked_sources AS (
        SELECT 
            st.sourceid,
            st.source,
            st.source_sum,
            ROW_NUMBER() OVER (ORDER BY st.source_sum DESC) AS rank
        FROM 
            source_totals st
    ), categorized_sources AS (
        -- Categorize sources contributing less than the cutoff as "Other"
        SELECT 
            st.sourceid,
            CASE 
                WHEN st.source_sum < {cutoff} * t.total_sum THEN -1.5
                WHEN st.rank >= {n_sources} THEN -1.5
                ELSE st.sourceid
            END AS revisedsourceid,
            CASE 
                WHEN st.source_sum < {cutoff} * t.total_sum THEN "Other"
                WHEN st.rank >= {n_sources} THEN "Other"
                ELSE st.source
            END AS source
        FROM 
            ranked_sources st
        CROSS JOIN 
            total_exportations t
    ), categorized_targets AS (
        -- Categorize targets contributing less than the cutoff as "Other"
        SELECT 
            tt.targetid,
            CASE 
                WHEN tt.target_sum < {cutoff} * t.total_sum THEN 1.5
                WHEN tt.rank >= {n_targets} THEN 1.5
                ELSE tt.targetid
            END AS revisedtargetid,
            CASE 
                WHEN tt.target_sum < {cutoff} * t.total_sum THEN "Other"
                WHEN tt.rank >= {n_targets} THEN "Other"
                ELSE tt.target
            END AS target
        FROM 
            ranked_targets tt
        CROSS JOIN 
            total_exportations t
    ), final_exportations AS (
        -- Recalculate exportations with categorized sources and targets
        SELECT
            cs.sourceid,
            cs.revisedsourceid,
            cs.source,
            ct.targetid,
            ct.revisedtargetid,
            ct.target,
            SUM(i.importations) AS region_sum
        FROM 
            `{table_name}` AS i
        JOIN 
            `{reference_table}` AS g_target 
            ON g_target.{reference_col} = i.{target_col}
        JOIN 
            `{reference_table}` AS g_source 
            ON g_source.{reference_col} = i.{source_col}
        JOIN 
            categorized_sources cs
            ON cs.sourceid = g_source.{source_resolution.split("_")[0]+"_id"} * -1
        JOIN 
            categorized_targets ct
            ON ct.targetid = g_target.{target_resolution.split("_")[0]+"_id"}
        WHERE 
            {where_clause}
            AND i.date >= "{date_range[0]}"
            AND i.date <= "{date_range[1]}"
        GROUP BY 
            cs.sourceid, 
            cs.revisedsourceid,
            cs.source, 
            ct.targetid, 
            ct.revisedtargetid,
            ct.target
    )
    -- Final query to return exportations, ensuring "Other" sources and targets are properly grouped
    SELECT
        fe.revisedsourceid AS sourceid,
        fe.source AS source,
        fe.revisedtargetid AS targetid,
        fe.target AS target,
        SUM(fe.region_sum) / (SELECT total_sum FROM total_exportations) AS exportations
    FROM 
        final_exportations fe
    GROUP BY 
        fe.revisedsourceid, 
        fe.source, 
        fe.revisedtargetid, 
        fe.target;
    """

    return query

def create_sankey_plot(data):
  # Create a set of unique node IDs from both sourceid and targetid
  unique_ids = set(data["sourceid"]).union(set(data["targetid"]))

  # Create mapping for indices
  dict_indices = {id_: idx for idx, id_ in enumerate(unique_ids)}

  # Create mapping for labels (using the first occurrence of each name)
  name_mapping = {}
  for idx, row in data.iterrows():
      name_mapping[row["sourceid"]] = row["source"]
      name_mapping[row["targetid"]] = row["target"]

  # Generate source, target, and value lists for the Sankey diagram
  source = data["sourceid"].map(dict_indices)
  target = data["targetid"].map(dict_indices)
  value = data["exportations"]

  # Create Sankey diagram
  fig = go.Figure(go.Sankey(
      node=dict(
          pad=15,
          thickness=20,
          line=dict(color="black", width=0),
          label=[name_mapping[id_] for id_ in dict_indices.keys()],  # Use names as node labels
      ),
      link=dict(
          source=source,  # Use mapped source indices
          target=target,  # Use mapped target indices
          value=value,
          color='rgba(221, 219, 215, .6)',
      )
  ))

  fig.update_layout(
      title_text = "Sankey Plot",
      template=netsi
      )
  
  # convert values to percentages and other formatting
  fig.data[0]["valueformat"] = ".1%"

  return fig

def sankey(client, table_name, reference_table, 
            source_geo_level, target_geo_level, 
            source_values, target_values, 
            date_range, value="importations",
           cutoff=0.05, source_resolution=None, target_resolution=None, domestic=True,
           source_column='source_basin', target_column='target_basin', reference_column='basin_id',
           n_sources=None, n_targets=None):
    """ Creates a sankey diagram to show flow of cases.
     
    Inputs:
        client (google.cloud.bigquery.Client): initialized BigQuery client
        table_name (str): BigQuery table name in "dataset.table" format containing importation data
        reference_table (str): BigQuery table name in "dataset.table" format containing GLEAM or LEAM-US geography mappings
        source_geo_level (str): a column in reference_table used to slice data by source, eg `region_label`
        target_geo_level (str): a column in reference_table used to slice data by target, eg `region_label`
        source_resolution (str): a column in reference_table, geographic resolution of source nodes. defaults to source_geo_level
        target_resolution (str): a column in reference_table, geographic resolution of target nodes. defaults to target_geo_level
        source_values (list or str): values of source_geo_level that will be included as source nodes, eg `Northern Europe`. set to None to include all. 
        target_values (list or str): values of target_geo_level that will be included as target nodes, eg `Northern Europe`. set to None to include all. 
        date_range (list of str): range of dates, inclusive, that will be visualized. formatted as "YYYY-MM-DD"
        domestic (bool): whether or not cases originating and ending in target_values will be included
        cutoff (float): any source or target geography contributing under the cutoff (between 0 and 1) will be aggregated into `Other`, defaults to 0.05
        
    Returns:
        fig (plotly.graph_objects.Figure): formatted sankey diagram
    """
    
    # Generate the query
    query = build_sankey_query(
        table_name=table_name,
        reference_table=reference_table,
        source_geo_level=source_geo_level,
        target_geo_level=target_geo_level,
        source_values=source_values,
        target_values=target_values,
        date_range=date_range,
        cutoff=cutoff,
        source_resolution=source_resolution,
        target_resolution=target_resolution,
        domestic=domestic,
        value=value,
        n_sources=n_sources,
        n_targets=n_targets,
        source_col=source_column, 
        target_col=target_column, 
        reference_col=reference_column,
    )
    
    # Execute the query to get the data
    data = execute(client, query)
    
    # Create and return the Sankey plot
    return create_sankey_plot(data)

def fetch_sankey_data(fig):
    source = fig.data[0].link.source
    target = fig.data[0].link.target
    value = fig.data[0].link.value
    df = pd.DataFrame({'source': source, 'target': target, 'value': value})
    df[['source', 'target']] = df[['source', 'target']].replace(dict(enumerate(fig.data[0].node.label)))
    return df



def build_bar_query(table_name, reference_table, source_geo_level, target_geo_level, source_values, target_values, 
                    date_range, value,
                    source_col='source_basin', target_col='target_basin', reference_col='basin_id',
                       cutoff=0.05, target_resolution=None, domestic=True, n=20,
                       categories=None, category_col='category'):
        
    if target_resolution == None:
        target_resolution = target_geo_level
                       
    # Build filters for both source and target regions
    source_filter = build_geographic_filter(source_geo_level, source_values, alias="g_source")
    target_filter = build_geographic_filter(target_geo_level, target_values, alias="g_target")
    cat_filter = build_categorical_filter(categories, category_col=category_col) if categories is not None else "TRUE"
    
    # Create the base where clause
    where_clauses = []

    if source_filter:
        where_clauses.append(source_filter)
    if target_filter:
        where_clauses.append(target_filter)
    if cat_filter:
        where_clauses.append(cat_filter)
            
    if not domestic:
        # Exclude rows where target imports to itself
        where_clauses.append(f"g_source.{target_resolution} != g_target.{target_resolution}")
        
    # Join the where clauses with "AND"
    where_clause = " AND ".join(where_clauses)
        
    query = f"""
        WITH total_exportations AS (
            -- Calculate total exportations for the given date range
            SELECT 
                SUM(i.{value}) AS total_sum
            FROM 
                `{table_name}` AS i
            JOIN 
                `{reference_table}` AS g_target 
                ON g_target.{reference_col} = i.{target_col}
            JOIN 
                `{reference_table}` AS g_source 
                ON g_source.{reference_col} = i.{source_col}
            WHERE 
                {where_clause}
                AND i.date >= "{date_range[0]}"
                AND i.date <= "{date_range[1]}"
        ), 
        target_totals AS (
            -- Calculate total exportations for each target
            SELECT
                g_target.{target_resolution.split("_")[0]+"_id"} AS targetid,
                g_target.{target_resolution} AS target,
                SUM(i.importations) AS target_sum
            FROM 
                `{table_name}` AS i
            JOIN 
                `{reference_table}` AS g_target 
                ON g_target.{reference_col} = i.{target_col}
            JOIN 
                `{reference_table}` AS g_source 
                ON g_source.{reference_col} = i.{source_col}
            WHERE 
                {where_clause}
                AND i.date >= "{date_range[0]}"
                AND i.date <= "{date_range[1]}"
            GROUP BY targetid, target
            ORDER BY target_sum DESC
        ), ranked_targets AS (
        -- Rank targets based on their target_sum
        SELECT 
            tt.targetid,
            tt.target,
            tt.target_sum,
            ROW_NUMBER() OVER (ORDER BY tt.target_sum DESC) AS rank
        FROM 
            target_totals tt
        ),categorized_targets AS (
        -- Categorize targets contributing less than the cutoff or outside the top n-1 as "Other"
        SELECT 
            rt.targetid,
            CASE 
                WHEN rt.target_sum < {cutoff} * t.total_sum THEN -1
                WHEN rt.rank >= {n} THEN -1
                ELSE rt.targetid
            END AS revisedtargetid,
            CASE 
                WHEN rt.target_sum < {cutoff} * t.total_sum THEN "Other"
                WHEN rt.rank >= {n} THEN "Other"
                ELSE rt.target
            END AS target,
            rt.target_sum
        FROM 
            ranked_targets rt
        CROSS JOIN 
            total_exportations t
    )

        -- Final query to sum importations for each target and group "Other" regions
        SELECT 
            ct.revisedtargetid AS targetid,
            ct.target AS target,
            SUM(ct.target_sum) / (SELECT total_sum FROM total_exportations) AS total_importations
        FROM 
            categorized_targets ct
        GROUP BY 
            targetid, target
        ORDER BY 
            total_importations DESC;

        """
    
    return query

def create_bar_chart(data: pd.DataFrame, title: str = "Relative Risk of Importation", ):
    fig = px.bar(
    data.iloc[:, :], x="total_importations", y="target", orientation="h", 
    labels={
        "target": "Target",
        "total_importations": "Relative Risk of Importation"
    },
    template="netsi"
)

# Sort y-axis by exportations with "Other" fixed at the bottom
    fig.update_layout(
        yaxis={"categoryorder": "array", "categoryarray": ["Other"] + sorted(
            [x for x in data["target"].unique() if x != "Other"],
            key=lambda target: data.loc[data["target"] == target, "total_importations"].sum(),
            reverse=False
        )},
        title={
            "text": title
            },
        showlegend=False
    )

    return fig

def relative_risk(client, table_name, reference_table, source_geo_level, target_geo_level, source_values, target_values, date_range, value="importations",
           cutoff=0.05, n=20, output_resolution=None, domestic=True, 
           source_column='source_basin', target_column='target_basin', reference_column='basin_id',
           ):
    
    """ Creates a sankey diagram to show flow of cases.
     
    Inputs:
        client (google.cloud.bigquery.Client): initialized BigQuery client
        table_name (str): BigQuery table name in "dataset.table" format containing importation data
        reference_table (str): BigQuery table name in "dataset.table" format containing GLEAM or LEAM-US geography mappings
        source_geo_level (str): a column in reference_table used to slice data by source, eg `region_label`
        target_geo_level (str): a column in reference_table used to slice data by target, eg `region_label`
        source_values (list or str): values of source_geo_level that will be included as source nodes, eg `Northern Europe`. set to None to include all. 
        target_values (list or str): values of target_geo_level that will be included as target nodes, eg `Northern Europe`. set to None to include all. 
        target_resolution (str): a column in reference_table, geographic resolution of target nodes. defaults to target_geo_level
        date_range (list of str): range of dates, inclusive, that will be visualized. formatted as "YYYY-MM-DD"
        domestic (bool): whether or not cases originating and ending in target_values will be included
        cutoff (float): any source or target geography contributing under the cutoff (between 0 and 1) will be aggregated into `Other`, defaults to 0.05
        n (int > 0): maximum number of rows to be displayed. all other rows will be aggregated into other, regardless of cutoff
        
    Returns:
        fig (plotly.graph_objects.Figure): formatted relative risk chart
    """

    # Generate the query
    query = build_bar_query(
        table_name=table_name,
        reference_table=reference_table,
        source_geo_level=source_geo_level,
        target_geo_level=target_geo_level,
        source_values=source_values,
        target_values=target_values,
        date_range=date_range,
        cutoff=cutoff,
        target_resolution=output_resolution,
        domestic=domestic,
        n=n,
        value=value,
        source_col=source_column, 
        target_col=target_column, 
        reference_col=reference_column,
    )
    
    # Execute the query to get the data
    data = execute(client, query)
    
    # Create and return the Sankey plot
    return create_bar_chart(data, )

def fetch_relative_risk_data(fig):
    df = pd.DataFrame({fig.layout.xaxis.title.text.lower().replace(" ", "_"): fig.data[0].x}, index=fig.data[0].y)
    return df