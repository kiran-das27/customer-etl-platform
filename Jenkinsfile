pipeline {
    agent {
        label 'docker-dynamic'
    }

    environment {
        DATABRICKS_HOST = credentials('databricks-host')
        DATABRICKS_TOKEN = credentials('databricks-token')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    echo "Python version:"
                    python3 --version

                    echo "Building application..."
                    python3 -m py_compile src/customer_job.py
                '''
            }
        }

        stage('Upload to Databricks') {
            steps {
                sh '''
                    echo "Creating application workspace directory..."

                    databricks workspace mkdirs /Workspace/Shared/customer-etl

                    echo "Uploading application..."

                    databricks workspace import-dir \
                        src \
                        /Workspace/Shared/customer-etl
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}