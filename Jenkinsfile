pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'krishnaves/hello-world-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        VAULT_ADDR = 'http://vault.vault.svc.cluster.local:8200'
        MESSAGE = "Hello from Jenkins build ${BUILD_NUMBER}"
    }

    stages {
        stage('Update Vault') {
            steps {
                script {
                    vaultToken = sh(script: 'kubectl exec -n vault vault-0 -- vault token create -field token',
                        returnStdout: true).trim()
                    sh """
                        kubectl exec -n vault vault-0 -- vault login ${vaultToken}
                        kubectl exec -n vault vault-0 -- vault kv put secret/app-config message="${MESSAGE}"
                    """
                }
            }
        }

        stage('Build') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }

        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials',
                    usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    """
                    }
            }
        }

        stage('Deploy') {
            steps {
                sh """
                    helm upgrade --install hello-world ./helm \
                        --namespace production \
                        --set image.repository=${DOCKER_IMAGE} \
                        --set image.tag=${DOCKER_TAG}
                """
            }
        }
    }
}
