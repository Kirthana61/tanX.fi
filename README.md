# tanX.fi - Task_21BCE5129

This Flask-based application processes a dataset and performs various analyses. It generates a CSV file with customer order data and computes the following metrics:
- Total revenue generated by a store for each month
- Total revenue generated by each product
- Total revenue generated by each customer
- Top _ customers by revenue generated

## Dockerization

The `Dockerfile` contains the instructions for building the Docker image for the Flask application. It includes the necessary configurations and setup required for running the application in a containerized environment.

### Building the Docker Image

To build the Docker image, run:

```sh
docker build -t task-21bce5129 .
```

### Pushing the Docker Image

To push the Docker image to the repository, use:

```sh
docker push kirthanabalaji/task-21bce5129:latest
```

### Usage

To pull the Docker image for this Flask application, use the following command:

```sh
docker pull kirthanabalaji/task-21bce5129:latest
```

### Requirements

The `requirements.txt` file lists all the Python packages and their versions required for the Flask application to run. Ensure that these packages are installed in the Docker container.

## Testing Instructions (Option 1)

The website is hosted on [Render](https://render.com/) with deployment settings executed using the `Dockerfile`. To test the application, follow these steps:

1. **Visit the Website:**
   [Link](https://tanx-fi.onrender.com/)

2. **Wait for the Page to Load:**
   Since the website is hosted on a free plan, it may take a few seconds to load. Please be patient.

3. **Upload a CSV File:**
   - Ensure the CSV file you upload has the same column names and format as the `orders.csv` file located in the test directory.

4. **Complete Required Actions:**
   - Make sure all mandatory selections and fields are completed as specified on the webpage.

## Testing Instructions (Option 2)

1. Pull the Docker image from the repository:

    ```sh
    docker pull kirthanabalaji/task-21bce5129:latest
    ```

2. Run the Docker container:

    ```sh
    docker run -d -p 5000:5000 kirthanabalaji/task-21bce5129
    ```

3. Visit the application in your web browser at:

    ```
    http://localhost:5000
    ```

