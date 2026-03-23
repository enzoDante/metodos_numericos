import sympy as sp
import math
class CalcErroArredondamento:
    def __init__(self):
        self.equation = ""        # equação de entrada do usuário
        self.expr = ""            # expressão matemática convertida
        self.f = ""               # uso da expressão como função
        self.intervaloStart = 0.0 # intervalo inicial
        self.intervaloEnd = 0.0   # intervalo final
        self.trapezios = 0        # quantidade de trapézios
        self.casasDecimais = 0    # casas decimais desejada
        self.altura = 0           # usada para calcular altura
        self.fatorAltura = 0      # altura dos trapézios
        self.calculo = 0          # somatório das áreas do trapézio
        self.tabela = ""          # tabela com os valores de x dentro do intervalo citado e com a função
        self.tabelaCriada = False # validação se a tabela foi ou não criada
        self.calcErro = False     # validação se o erro de arredondamento foi ou não calculado
        self.receberDadosdoProblema() # função para usuário inserir os dados de entrada
        self.calculoTrap()            # função para calcular a altura dos trapézio
        self.menu()                   # menu de opções para o usuário
    
    def createEqua(self, expressao: str):
        # está função converte qualquer string em expressão matemática para ser usada no código
        x = sp.Symbol('x')
        expr = sp.sympify(expressao)  # Interpreta a string como expressão simbólica
        f = sp.lambdify(x, expr, modules='numpy')
        return f, expr

    def receberDadosdoProblema(self):
        # usuário deve digitar os dados de entrada desejado
        while True:
            try:
                self.equation = input("Digite a função:")
                self.f, self.expr = self.createEqua(self.equation)
                break
            except:
                print("ERRO! DIGITE A FUNÇÃO CORRETAMENTE!")
        while True:
            try:
                self.intervaloStart = float(input("Digite o valor inicial do intervalo:"))
                break
            except:
                print("ERRO! DIGITE APENAS NÚMEROS!")
        while True:
            try:
                self.intervaloEnd = float(input("Digite o valor final do intervalo:"))
                break
            except:
                print("ERRO! DIGITE APENAS NÚMEROS!")
        while True:
            try:
                self.trapezios = int(input("Digite a quantidade de trapézios:"))
                break
            except:
                print("ERRO! DIGITE APENAS NÚMEROS!")
        while True:
            try:
                self.casasDecimais = int(input("Digite a quantidade de casas decimais desejada para as respostas"))
                break
            except:
                print("ERRO! DIGITE APENAS NÚMEROS!")
    
    def calculoTrap(self):
        # função para calcular a altura dos trapézio
        self.altura = self.intervaloEnd - self.intervaloStart
        self.fatorAltura = self.altura / self.trapezios
        print(f"A altura de cada Trapézio (eixo X) consiste na razão entre a diferença \ndos valores do intervalo e o número de trapézios declarado!")
    
    def criarTabela(self):
        # criação da tabela com os dados dentro do limite do intervalo digitado pelo usuário e seus respectivos valores da função
        i = 0
        aux = []
        equat = []
        soma = 0
        aux.append(self.intervaloStart) # insere valor inicial do intervalo

        construirTabela = ""
        for i in range(0, self.trapezios+1): # percorre todos os trapézios dentro do intervalo
            equat.append(self.f(aux[i]))     # adiciona o valor de f(x) na lista
            if i < self.trapezios:
                aux.append(aux[i] + self.fatorAltura) # adiciona o fator em x exemplo: x = 2 --> x = 2.5 assim por diante
        # equat[0] = equat[0] / 2 
        # equat[self.trapezios] = equat[self.trapezios] /2
        construirTabela = "  X              f(X) \n"
        for i in range(0, self.trapezios+1): # construção da tabela visual para o usuário
            # soma += raizQuad[i]
            soma += equat[i]
            construirTabela += f"  {aux[i]:.{self.casasDecimais}f}       {equat[i]:.{self.casasDecimais}f}\n"
        construirTabela += "-----------------------\n"
        construirTabela += f"Soma = {soma:.{self.casasDecimais}f}"
        self.tabela = construirTabela
        self.tabelaCriada = True
    
    def exibirTabela(self):
        if not self.tabelaCriada:
            print("ERRO! A TABELA AINDA NÃO FOI CRIADA!")
            return
        print(self.tabela)
    
    def calcErroArred(self):
        self.calculo = 0
        aux = []
        aux.append(self.intervaloStart) # adiciona inicio do intervalo em aux
        soma = 0
        equat = []
        for i in range(0, self.trapezios+1): # percorre os trapézios e adicionar o valor de f(x) em equat[]
            equat.append(self.f(aux[i]))
            if(i < self.trapezios):
                aux.append(aux[i] + self.fatorAltura) # adiciona o fator em x exemplo: x = 2 --> x = 2.5 assim por diante
        
        for i in range(0, self.trapezios): # somatório das áreas dos trapézios
            self.calculo += ((equat[i+1] + equat[i]) / 2) * self.fatorAltura
            
        temp = round(self.calculo * math.pow(10, self.casasDecimais))
        ultimaCasa = int(temp % 10)
        vlArred = 0.5 * math.pow(10, -self.casasDecimais) # valor de arredondamento para calcular o erro
        erroArredondamento = self.trapezios * vlArred * self.fatorAltura # erro de arredondamento
        self.calcErro = True
        print(f"|Ea| <= {self.trapezios} * {vlArred:.{self.casasDecimais+1}f} * {self.fatorAltura:.{self.casasDecimais}f} = {erroArredondamento:.{self.casasDecimais+1}f}")

    def getNumTrap(self):
        print(f"Número de Trapézios = {self.trapezios}")
    def getCasasDecimais(self):
        print(f"Número de Casas Decimais = {self.casasDecimais}")
    def getAlturaCadaTrap(self):
        print(f"Altura de cada Trapézio = {self.fatorAltura}")
    def getInicioIntervalo(self):
        print(f"Valor de início do intervalo = {self.intervaloStart}")
    def getFimIntervalo(self):
        print(f"Valor do fim do intervalo = {self.intervaloEnd}")
    def getValorSomatorio(self):
        if not self.calcErro:
            print(f"ERRO! A SOMATÓRIA AINDA NÃO FOI CALCULADA!")
            return
        print(f"Resultado do Somatório = {self.calculo:.{self.casasDecimais}f}")

    def menu(self):
        while True:
            try:
                escolha = int(input("=== MENU ===\n" +
                                "1 - Calcula Erro de Arredondamento\n" +
                                "2 - Criar Tabela de 'x' e 'f(x)'\n" +
                                "3 - Exibir Tabela\n" +
                                "4 - Dados do Problema\n" +
                                "0 - Sair\n\n" +
                                "Escolha uma opção:\n"))
                if escolha == 0:
                    break
                elif escolha == 1:
                    self.calcErroArred()
                elif escolha == 2:
                    self.criarTabela()
                    print("Tabela de valores criada e preenchida com sucesso!")
                elif escolha == 3:
                    self.exibirTabela()
                elif escolha == 4:
                    self.getInicioIntervalo()
                    self.getFimIntervalo()
                    self.getNumTrap()
                    self.getCasasDecimais()
                    self.getAlturaCadaTrap()
                    self.getValorSomatorio()

            except:
                print("Erro, selecione uma opção corretamente")

CalcErroArredondamento()

    