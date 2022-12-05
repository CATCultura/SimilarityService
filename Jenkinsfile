pipeline {
    agent any

    stages {
//         stage('Test') {
//             steps {
//                 sh 'python3 -m unittest '
//             }
//         }

        stage('Deploy') {
            when {branch 'main'}
                steps {
    //                 sh 'sudo docker kill $(sudo docker ps -q -f ancestor=similarity-service)'
    //                 sh 'sudo docker rmi similarity-service -f'
                    sh 'sudo docker build -t similarity-service .'
    //                 sh 'sudo docker run -d -p 5500:5500 -v dataset-json-repo:/py-service/data similarity-service'
                }
            }

       stage('Notify') {
           steps {
              discordSend description: "Similarity service successful build", footer: "Results from a build", link: env.BUILD_URL, result: currentBuild.currentResult, title: JOB_NAME, webhookURL: "https://discord.com/api/webhooks/1029023402079572108/PSi21wQLj8EdmwAYw6DbyEsGuppRKibwV7r81QVq743lG5Z3_qZw2vNIr5jJ_sU_15RZ"
           }
        }

    }
}