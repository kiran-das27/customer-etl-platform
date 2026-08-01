pipeline {

    agent {
        label 'jenkins-k8s-agent'
        }

    environment {
            AWS_REGION = 'us-east-1'
            ECR_REPO = 'customer-etl'
            ECR_URI = '082787299786.dkr.ecr.us-east-1.amazonaws.com/customer-etl'
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

    }
}