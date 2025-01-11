

#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI All Paths 
from softwareai.CoreApp._init_paths_ import *
#########################################
# IMPORT SoftwareAI Instructions
from softwareai.CoreApp.SoftwareAI.Instructions._init_Instructions_ import *
#########################################
# IMPORT SoftwareAI Tools
from softwareai.CoreApp.SoftwareAI.Tools._init_tools_ import *
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *
#########################################
# IMPORT SoftwareAI _init_environment_
from softwareai.CoreApp._init_environment_ import init_env


class CodeFlux:
    def __init__(self, 
                Company_Managers,
                Pre_Project_Document,
                Gerente_de_projeto,
                Equipe_De_Solucoes,
                Softwareanaysis,
                SoftwareDevelopment,
                ):
        
        self.Company_Managers = Company_Managers
        self.Pre_Project_Document = Pre_Project_Document
        self.Gerente_de_projeto = Gerente_de_projeto
        self.Equipe_De_Solucoes = Equipe_De_Solucoes
        self.Softwareanaysis = Softwareanaysis
        self.SoftwareDevelopment = SoftwareDevelopment

        self.name_app = "appx"
        self.key_openai = OpenAIKeysteste.keys()
        self.appfb = FirebaseKeysinit._init_app_(name_app)
        self.client = OpenAIKeysinit._init_client_(key_openai)




    
    def CodeFlux_Company_Owners(self,mensagem, repo_name):


        instructionCodeFlux = """

        """
        adxitional_instructions = """

        """


        key = "AI_CodeFlux_Company_Owners"
        nameassistant = "AI CodeFlux Donos da Empresa Urobotsoftware"
        model_select = "gpt-4o-mini-2024-07-18"

        vectorstore_in_assistant = None 
        vectorstore_in_Thread = None
        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_1_image_for_vision_in_thread = None
        Upload_list_for_code_interpreter_in_thread = None

        AI_CodeFlux, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(self.appfb, self.client, key, instructionCodeFlux, nameassistant, model_select)


        repo_name = f"A-I-O-R-G/{repo_name}" 
        branch_name = "main"  # Substitua pelo branch correto, se necessário

        onlyrepo_name = repo_name.replace("A-I-O-R-G/", "")
        AnalysisRequirements = self.get_file_content(repo_name, "AppMap/Analisys/AnalysisRequirements.txt", branch_name)




        mensaxgem = f"""decida oque o usuario esta solicitando com base na mensagem asseguir: {mensagem} \n       
        
        """  

        regra1 = "Regra 1 - Caso seja solicitado algum script ou software Responda no formato JSON Exemplo: {'solicitadoalgumcodigo': 'solicitacao...'} "

        regra2 = "Regra 2 - Caso seja solicitado alguma atualização de repositorio de software Responda no formato JSON Exemplo: {'solicitadoatualizaçãoderepositoriosoftware': 'somente o nome do repositorio que o usuario informou'} "
            
        mensaxgemfinal = mensaxgem + regra1 + regra2
        
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensaxgemfinal,
                                                                agent_id=AI_CodeFlux, 
                                                                key=key,
                                                                app1=self.appfb,
                                                                client=self.client,
                                                                tools=[{ "type": "file_search" }, { "type": "code_interpreter" }],
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions)
                                                
                                
         
                                            
        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensaxgemfinal, response, instructionsassistant, nameassistant)
        
        print(response)
        try:
            teste_dict = json.loads(response)
        except:
            teste_dict = response


    def get_file_content(self, repo_name, file_path, branch_name):

        github_username, github_token = GithubKeys.QuantumCore_github_keys()

        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
  

        file_url = f"https://api.github.com/repos/{repo_name}/contents/{file_path}?ref={branch_name}"
        response = requests.get(file_url, headers=headers)
        
        if response.status_code == 200:
            file_data = response.json()
            import base64
            content = base64.b64decode(file_data['content']).decode('utf-8')
            return content
        else:
            print(f"Erro ao acessar {file_path}. Status: {response.status_code}  {response.content}")
            return None
        



