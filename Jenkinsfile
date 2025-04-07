pipeline {
    agent any

    environment {
		BASE_DIR = 'D:\software_engineer\Graduation_Design\testcase\rjgc\'
        ALLURE_RESULTS = 'result'
        ALLURE_REPORT = 'report'
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Code checked out'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                script {
					bat '''
						if not exist "%BASE_DIR%venv" (
							python -m venv %BASE_DIR%venv
						)
						call %BASE_DIR%\\venv\\Scripts\\activate
					'''
                }
            }
        }

        stage('Run Tests with Pytest') {
            steps {
                script {
					bat '''
						call %BASE_DIR%\\venv\\Scripts\\activate
						pytest -m "login" -n 3 --alluredir=%ALLURE_RESULTS% --clean-alluredir
						pytest -m "personal_info" --alluredir=%ALLURE_RESULTS%
					'''
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
					bat '''
						call %BASE_DIR%\\venv\\Scripts\\activate
						allure generate %ALLURE_RESULTS% -o %ALLURE_REPORT% --clean
					'''
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: "${ALLURE_REPORT}/**", allowEmptyArchive: true
            echo 'Build completed'
        }
    }
}
