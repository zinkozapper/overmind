pipeline {
    agent any

    environment {
        REGISTRY = "ghcr.io"
        ORG = "zinkozapper"
        IMAGE_NAME = "overmind"
        CREDENTIAL_ID = "zinko-github"
        FLEET_REPO = "engineering-fleet"
        SC2PATH = "/StarCraftII"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Diagnostics') {
            steps {
                // This will tell us if Jenkins can actually run Docker
                sh 'docker version'
            }
        }
    }
}

'''
        stage('Build Frontend Image') {
            steps {
                sh """
                    docker build \
                      -t ${REGISTRY}/${ORG}/${IMAGE_NAME} \
                      -f Dockerfile .
                """
            }
        }

        stage('Login to GHCR') {
            steps {
                withCredentials([usernamePassword(
                        credentialsId: env.CREDENTIAL_ID,
                        usernameVariable: 'GHCR_USER',
                        passwordVariable:'GHCR_TOKEN'
                    )]) {
                    sh """
                        echo $GHCR_TOKEN | docker login ${REGISTRY} -u $GHCR_USER --password-stdin
                    """
                }
            }
        }

        stage('Push Image') {
            steps {
                sh """
                    docker push ${REGISTRY}/${ORG}/${IMAGE_NAME}
                """
            }
        }

        stage('Get Image Digest') {
            steps {
                script {
                    env.IMAGE_DIGEST = sh(
                        script: "docker buildx imagetools inspect ${REGISTRY}/${ORG}/${IMAGE_NAME} --format '{{json .Manifest.Digest}}' | tr -d '\"'",
                        returnStdout: true
                    ).trim()

                    echo "Image digest: ${env.IMAGE_DIGEST}"
                }
            }
        }

        stage('Update Fleet Repo') {
            when {
                anyOf {
                    branch 'main'
                    branch 'development'
                }
            }

            steps {
                withCredentials([usernamePassword(
                        credentialsId: env.CREDENTIAL_ID,
                        usernameVariable: 'GIT_USER',
                        passwordVariable:'GIT_TOKEN'
                )]) {

                    sh """
                        rm -rf fleet-repo
                        git clone https://\$GIT_USER:\$GIT_TOKEN@github.com/${ORG}/${FLEET_REPO}.git fleet-repo
                        cd fleet-repo
                        git config user.name "jenkins-bot"
                        git config user.email "jenkins-bot@byu.edu"
                        git checkout main
                        git pull origin main
                    """

                    script {
                        def branchFolder = (env.BRANCH_NAME == 'development') ? "beta" : "main"

                        sh """
                            set -e
                            cd fleet-repo/${branchFolder}

                            IMAGE_FILE=\$(find . -type f -name "${IMAGE_NAME}.yml" | head -n 1)
                            if [ -n "\$IMAGE_FILE" ]; then
                                sed -i "s|image: ${REGISTRY}/${ORG}/${IMAGE_NAME}.*|image: ${REGISTRY}/${ORG}/${IMAGE_NAME}@${IMAGE_DIGEST}|" "\$IMAGE_FILE"
                            else
                                echo "No ${IMAGE_NAME}.yml file found!"
                                exit 1
                            fi
                        """

                        sh """
                            cd fleet-repo
                            git add .

                            if ! git diff --cached --quiet; then
                                git commit -m "Update ${IMAGE_NAME} image to ${IMAGE_DIGEST}"
                                git push https://\$GIT_USER:\$GIT_TOKEN@github.com/${ORG}/${FLEET_REPO}.git main
                                echo "Fleet repo updated."
                            else
                                echo "No changes to commit."
                            fi
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout ghcr.io || true'
        }
    }
}
'''