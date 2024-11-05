def img
pipeline {
	environment {
    	registry = "dfortysix/shop_cicd"
    	registryCredential = 'Dockerhub-xacthuc'
    	dockerImage = ''
	}
	agent any
	stages {
    	stage('checkout') {
        	steps {
            	 git branch: 'main', url: 'https://github.com/Dfortysix/Shiro-shop.git'
        	}
    	}

    	stage ('Stop previous running container'){
        	steps{
            	sh returnStatus: true, script: 'docker stop $(docker ps -a | grep ${JOB_NAME} | awk \'{print $1}\')'
            	sh returnStatus: true, script: 'docker rmi $(docker images | grep ${registry} | awk \'{print $3}\') --force' //this will delete all images
            	sh returnStatus: true, script: 'docker rm ${JOB_NAME}'
        	}
    	}


    	stage('Build Image') {
        	steps {
            	script {
                	img = registry + ":${env.BUILD_ID}"
                	println ("${img}")
                	dockerImage = docker.build("${img}")
            	}
        	}
    	}



    	stage('Test - Run Docker Container on Server Test') {
       	steps {

            	sh label: '', script: "docker run -d --name ${JOB_NAME} -p 7999:8000 ${img}"
      	}
    	}

    	stage('Push Image To DockerHub') {
        	steps {
            	script {
                	docker.withRegistry( 'https://registry.hub.docker.com ', registryCredential ) {
                    	dockerImage.push()
                	}
            	}
        	}
    	}


        stage('Deploy to Server Production') {
            steps {
                script {
                    def stopcontainer = "docker stop ${JOB_NAME}"
                    def delcontName = "docker rm ${JOB_NAME}"
                    def delimages = 'docker image prune -a --force'
                    def drun = "docker run -d --name ${JOB_NAME} -p 80:8000 ${img}"
                    def add_pub_ss = "13.250.6.249"
                    println "${drun}"
                    sshagent(['staging-key']) {
                        sh returnStatus: true, script: "ssh -o StrictHostKeyChecking=no ubuntu@${add_pub_ss} ${stopcontainer} "
                        sh returnStatus: true, script: "ssh -o StrictHostKeyChecking=no ubuntu@${add_pub_ss} ${delcontName}"
                        sh returnStatus: true, script: "ssh -o StrictHostKeyChecking=no ubuntu@${add_pub_ss} ${delimages}"

                        // some block
                        sh "ssh -o StrictHostKeyChecking=no ubuntu@${add_pub_ss} ${drun}"
                    }
                }
            }
        }


	}
}