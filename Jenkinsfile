pipeline {

    agent {
        label 'jenkins-k8s-agent'
    }

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO   = 'customer-etl'
        ECR_URI    = '082787299786.dkr.ecr.us-east-1.amazonaws.com/customer-etl'
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
                sh 'python3 --version'
                sh 'pip3 --version'
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

        stage('Build and Push Docker Image') {
            steps {
                container('kaniko') {
                    sh '''
                        /kaniko/executor \
                            --context "${WORKSPACE}" \
                            --dockerfile "${WORKSPACE}/Dockerfile" \
                            --destination "${ECR_URI}:${BUILD_NUMBER}" \
                            --destination "${ECR_URI}:latest"
                    '''
                }
            }
        }

        stage('Verify Artifact') {
            steps {
                sh 'ls -R dist'
            }
        }

        stage('Verify Databricks CLI') {
            steps {
                sh 'databricks version'
            }
        }

        stage('Verify Databricks Connection') {
            steps {
                withCredentials([
                    string(credentialsId: 'databricks-host', variable: 'DATABRICKS_HOST'),
                    string(credentialsId: 'databricks-token', variable: 'DATABRICKS_TOKEN')
                ]) {
                    sh '''
                        echo "Testing Databricks connection..."

                        export DATABRICKS_HOST="${DATABRICKS_HOST}"
                        export DATABRICKS_TOKEN="${DATABRICKS_TOKEN}"

                        databricks workspace list /
                    '''
                }
            }
        }

        stage('Deploy Python Application') {
            steps {
                withCredentials([
                    string(credentialsId: 'databricks-host', variable: 'DATABRICKS_HOST'),
                    string(credentialsId: 'databricks-token', variable: 'DATABRICKS_TOKEN')
                ]) {
                    sh '''
                        export DATABRICKS_HOST="${DATABRICKS_HOST}"
                        export DATABRICKS_TOKEN="${DATABRICKS_TOKEN}"

                        echo "Creating application workspace directory..."

                        databricks workspace mkdirs /Workspace/Shared/customer-etl

                        echo "Uploading application source..."

                        databricks workspace import \
                            src/customer_job.py \
                            /Workspace/Shared/customer-etl/customer_job.py \
                            --language PYTHON \
                            --overwrite
                    '''
                }
            }
        }

        stage('Deploy Wheel') {
            steps {
                withCredentials([
                    string(credentialsId: 'databricks-host', variable: 'DATABRICKS_HOST'),
                    string(credentialsId: 'databricks-token', variable: 'DATABRICKS_TOKEN')
                ]) {
                    sh '''
                        export DATABRICKS_HOST="${DATABRICKS_HOST}"
                        export DATABRICKS_TOKEN="${DATABRICKS_TOKEN}"

                        echo "Uploading Python wheel..."

                        databricks workspace import-dir \
                            dist \
                            /Workspace/Shared/customer-etl/dist \
                            --overwrite
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                withCredentials([
                    string(credentialsId: 'databricks-host', variable: 'DATABRICKS_HOST'),
                    string(credentialsId: 'databricks-token', variable: 'DATABRICKS_TOKEN')
                ]) {
                    sh '''
                        export DATABRICKS_HOST="${DATABRICKS_HOST}"
                        export DATABRICKS_TOKEN="${DATABRICKS_TOKEN}"

                        echo "Verifying Databricks deployment..."

                        databricks workspace list \
                            /Workspace/Shared/customer-etl
                    '''
                }
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

