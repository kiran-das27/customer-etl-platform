pipeline {

    agent {
        label 'jenkins-k8s-agent'
    }

    environment {
        AWS_REGION = 'us-east-1'
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

                    echo "OS:"
                    cat /etc/os-release | head

                    echo "Python:"
                    python3 --version
                '''
            }
        }

        stage('Verify Artifact') {
            steps {
                sh 'ls -lh dist/'
            }
        }

        stage('Check Databricks CLI') {
            steps {
                sh '''
                    databricks --version || true
                '''
            }
        }
    }
}

