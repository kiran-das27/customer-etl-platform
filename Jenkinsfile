pipeline {

    agent any

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

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build \
                    -t customer-etl:${BUILD_NUMBER} .
                    """
             }
        }

        stage('Verify Artifact') {
            steps {
                sh 'ls -R dist'
            }
        }

    }
}