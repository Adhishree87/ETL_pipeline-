# ETL Pipeline

It contains an ETL pipeline designed to fetch earthquake data from the USGS Earthquake API, transform it, and load it into a PostgreSQL database. The pipeline is built using Apache Airflow for orchestration and Docker for containerization.Later, the analysis and visualization is carried out using matplotlib , pandas and seaborn.

## How to Run It

1. **Start the Application:**
   - Run the following command to start the Airflow environment:
     ```bash
     astro dev start
     ```

2. **Set Up Connections in Airflow Web UI:**

   - **Access Airflow Web UI:**
     - Open `http://localhost:8080` in your browser.

   - **Go to Connections:**
     - Click on **Admin** > **Connections** in the Airflow UI.

   - **Add PostgreSQL Connection:**
     - Click **+** to add a new connection:
       - **Conn Id**: Fill in the connection ID.
       - **Conn Type**: Select `Postgres`.
       - **Host**: Fill in the host.
       - **Schema**: Fill in the schema.
       - **Login**: Fill in the login.
       - **Password**: Fill in the password.
       - **Port**: Fill in the port.
     - Click **Save**.

   - **Add USGS API Connection:**
     - Click **+** to add another connection:
       - **Conn Id**: Fill in the connection ID.
       - **Conn Type**: Select `HTTP`.
       - **Host**: Fill in the host.
     - Click **Save**.

3. **Run the Pipeline:**
   - Once the connections are set up, run your DAG in Airflow to fetch earthquake data and load it into PostgreSQL.
  
4 **Install DBeaver**: Download from [DBeaver website](https://dbeaver.io/download/).
**Create New Connection**: Select **PostgreSQL**, then **Next**.
 **Enter Details as required**: 
 **Test & Finish**: Click **Test Connection**, then **Finish**.
