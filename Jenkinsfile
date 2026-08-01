pipeline {

    agent {
        label 'jenkins-k8s-agent'
    }

    environment {
        AWS_REGION = 'us-east-1'
        DATABRICKS_HOST = credentials('databricks-host')
        DATABRICKS_TOKEN = credentials('databricks-token')
    }

    stages {

        stage('Checkout Verification') {
            steps {
                echo 'Repository checked out successfully.'
                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('Python Version') {
            steps {
                sh '''
                    python3 --version
                    pip3 --version
                '''
            }
        }

        stage('Validate Application') {
            steps {
                sh '''
                    python3 -m py_compile src/customer_job.py
                    echo "Python application validation successful."
                '''
            }
        }

        stage('Build Wheel') {
            steps {
                sh 'python3 setup.py bdist_wheel'
            }
        }

        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'dist/*.whl', fingerprint: true
            }
        }

        stage('Verify AWS Identity') {
            steps {
                sh 'aws sts get-caller-identity'
            }
        }

        stage('Verify Kubernetes Agent') {
            steps {
                sh '''
                    echo "Running inside Kubernetes Jenkins agent"
                    echo "Hostname:"
                    hostname

                    echo "Python:"
                    python3 --version

                    echo "Databricks CLI:"
                    databricks --version
                '''
            }
        }

        stage('Verify Databricks Connection') {
            steps {
                sh '''
                    export DATABRICKS_HOST="${DATABRICKS_HOST}"
                    export DATABRICKS_TOKEN="${DATABRICKS_TOKEN}"

                    echo "Testing Databricks connection..."
                    databricks workspace list /
                '''
            }
        }

        stage('Deploy Python Application') {
            steps {
                sh '''
                    export DATABRICKS_HOST="${DATABRICKS_HOST}"
                    export DATABRICKS_TOKEN="${DATABRICKS_TOKEN}"

                    echo "Creating application workspace directory..."

                    databricks workspace mkdirs \
                        /Workspace/Shared/customer-etl

                    echo "Uploading application..."

                    databricks workspace import \
                        /Workspace/Shared/customer-etl/customer_job.py \
                        --file src/customer_job.py \
                        --format SOURCE \
                        --overwrite

                    echo "Application uploaded successfully."
                '''
            }
        }

        stage('Deploy Wheel') {
            steps {
                sh '''
                    export DATABRICKS_HOST="${DATABRICKS_HOST}"
                    export DATABRICKS_TOKEN="${DATABRICKS_TOKEN}"

                    WHEEL=$(find dist -name "*.whl" | head -1)

                    echo "Uploading wheel: ${WHEEL}"

                    databricks workspace import \
                        /Workspace/Shared/customer-etl/$(basename "${WHEEL}") \
                        --file "${WHEEL}" \
                        --format AUTO \
                        --overwrite

                    echo "Wheel uploaded successfully."
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    export DATABRICKS_HOST="${DATABRICKS_HOST}"
                    export DATABRICKS_TOKEN="${DATABRICKS_TOKEN}"

                    echo "Databricks workspace contents:"
                    databricks workspace list \
                        /Workspace/Shared/customer-etl
                '''
            }
        }

        stage('Verify Artifact') {
            steps {
                sh 'ls -lh dist/'
            }
        }
    }
}

