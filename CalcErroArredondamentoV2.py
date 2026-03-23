import sympy as sp
import math

class CalcErroArredondamento:
    def __init__(self):
        self.equacao = ""             # Equação de entrada do usuário
        self.expr = ""                # Expressão matemática convertida
        self.funcao = ""              # Uso da expressão como função
        self.intervaloInicio = 0.0    # Intervalo inicial
        self.intervaloFim = 0.0       # Intervalo final
        self.trapezios = 0            # Quantidade de trapézios
        self.casasDecimais = 0        # Casas decimais desejada
        self.calculo = 0              # Somatório das áreas do trapézio
        self.fatorAltura = 0          # Altura dos trapézios
        self.erroArredondamento = 0   # Erro de arredondamento
        self.erroTruncamento = 0      # Erro de truncamento
        self.tabela = ""              # Tabela com os valores de x dentro do intervalo citado e com a função
        self.receberDadosdoProblema() # Função para usuário inserir os dados de entrada
        self.calculoTrap()            # Função para calcular a altura dos trapézio
        self.saida()                  # saida de opções para o usuário
    
    def criarEquacao(self, expressao: str):
        # Esta função converte qualquer string em expressão matemática para ser usada no código
        x = sp.Symbol('x')
        expr = sp.sympify(expressao)  # Interpreta a string como expressão simbólica
        funcao = sp.lambdify(x, expr, modules='numpy')
        return funcao, expr
    
    def calcularMaxSegundaDerivada(self, expr, a:float, b:float):
        x = sp.symbols('x')
        segunda_derivada = sp.diff(expr, x, 2) # Segunda derivada de f(x)
        # mod_segunda_derivada = sp.diff(segunda_derivada, x, 2) # Módulo da segunda derivada
        modulo = sp.Abs(segunda_derivada)

        # derivada do módulo |f''(x)|'
        derivada_modulo = sp.diff(modulo, x) # Derivada do módulo da segunda derivada
        try:
            pontos_criticos = sp.solve(derivada_modulo, x) # Encontrar os pontos críticos da derivada do módulo
            pontos_criticos = [
                float(p.evalf()) for p in pontos_criticos if p.is_real and a <= float(p.evalf()) <= b
            ]
        except:
            pontos_criticos = []
        candidatos = [a, b] + pontos_criticos # Candidatos a máximos da segunda derivada
        # avalia |f''(x)| em cada candidato e retorna o maior
        f_modulo = sp.lambdify(x, modulo, modules='numpy')
        maior_valor = max(abs(f_modulo(p)) for p in candidatos)
        return maior_valor

    def receberDadosdoProblema(self):
        # Usuário deve digitar os dados de entrada desejado
        while True:
            try:
                self.equacao = input("Digite a função do problema: ")
                self.funcao, self.expr = self.criarEquacao(self.equacao)
                break
            except Exception:
                print("\nERRO! DIGITE A FUNÇÃO CORRETAMENTE!\n")
        while True:
            try:
                self.intervaloInicio = float(input("Digite o valor inicial do intervalo: "))
                break
            except:
                print("\nERRO! DIGITE APENAS NÚMEROS!\n")
        while True:
            try:
                self.intervaloFim = float(input("Digite o valor final do intervalo: "))
                if self.intervaloFim <= self.intervaloInicio:
                    print("\nERRO! O VALOR FINAL DO INTERVALO DEVE SER MAIOR QUE O INICIAL!\n")
                    continue
                break
            except:
                print("\nERRO! DIGITE APENAS NÚMEROS!\n")
        while True:
            try:
                self.trapezios = int(input("Digite a quantidade de trapézios: "))
                if self.trapezios <= 0:
                    print("\nERRO! DIGITE UMA QUANTIDADE POSITIVA DE TRAPÉZIOS!\n")
                    continue
                break
            except:
                print("\nERRO! DIGITE APENAS NÚMEROS!\n")
        while True:
            try:
                self.casasDecimais = int(input("Digite a quantidade de casas decimais desejada para as respostas: "))
                if self.casasDecimais <= 0:
                    print("\nERRO! DIGITE UM NÚMERO POSITIVO!\n")
                    continue
                break
            except:
                print("\nERRO! DIGITE APENAS NÚMEROS!\n")
    
    def calculoTrap(self):
        # Função para calcular a altura dos trapézio
        altura = self.intervaloFim - self.intervaloInicio
        self.fatorAltura = altura / self.trapezios
        print(f"\nA altura de cada Trapézio (eixo X) consiste na razão entre a diferença \ndos valores do intervalo e o número de trapézios declarado!\n")

    def criarTabela(self):
        # Criação da tabela com os dados dentro do limite do intervalo digitado pelo usuário e seus respectivos valores da função
        col_X = []
        col_Fx = []
        soma = 0
        col_X.append(self.intervaloInicio) # Insere valor inicial do intervalo

        construirTabela = ""
        for i in range(0, self.trapezios+1): # Percorre todos os trapézios dentro do intervalo
            col_Fx.append(self.funcao(col_X[i]))     # Adiciona o valor de f(x) na lista
            if i < self.trapezios:
                col_X.append(col_X[i] + self.fatorAltura) # Adiciona o fator em x | Exemplo: x = 2 --> x = 2.5 assim por diante

        construirTabela = "    X          f(X) \n"
        for i in range(0, self.trapezios+1): # Construção da tabela visual para o usuário
            soma += col_Fx[i]
            construirTabela += f"  {col_X[i]:.{self.casasDecimais}f}       {col_Fx[i]:.{self.casasDecimais}f}\n"
        construirTabela += "-----------------------\n"
        construirTabela += f"              {soma:.{self.casasDecimais}f}"
        self.tabela = construirTabela
        print("\nTABELA DE VALORES DE X E f(X):\n")
        print(self.tabela)
    
    def calcSomaErroIntervalo(self):
        valores_X = []
        self.calculo = 0
        valores_X.append(self.intervaloInicio) # Adiciona inicio do intervalo em valores_X[]
        valores_Fx = []
        for i in range(0, self.trapezios+1): # Percorre os trapézios e adiciona o valor de f(x) em valores_Fx[]
            valores_Fx.append(self.funcao(valores_X[i]))
            if(i < self.trapezios):
                valores_X.append(valores_X[i] + self.fatorAltura) # Adiciona o fator em x | Exemplo: x = 2 --> x = 2.5 assim por diante
        
        print(f"A(tr) = {self.fatorAltura} * (", end="")
        for i in range(0, self.trapezios+1): # Somatório das áreas dos trapézios
            if i == 0 or i == self.trapezios:
                self.calculo += (valores_Fx[i] / 2)
                print(f"{valores_Fx[i]:.{self.casasDecimais}f}/2", end="") # O primeiro e o último termo da soma devem ser divididos por 2, pois são os extremos do intervalo
            else:
                self.calculo += valores_Fx[i]
                print(f"{valores_Fx[i]:.{self.casasDecimais}f}", end="") # Os termos intermediários são somados normalmente
            if i < self.trapezios:
                print(" + ", end="")
        print(")", end="")
        print(f" = {self.calculo:.{self.casasDecimais}f} * {self.fatorAltura:.{self.casasDecimais}f}", end="")
        
        # Multiplica o somatório pelo fator de altura para obter a área total aproximada sob a curva
        self.calculo *= self.fatorAltura 
        print(f" = {self.calculo:.{self.casasDecimais}f}\n")
        vlArred = 0.5 * math.pow(10, -self.casasDecimais) # Valor de arredondamento para calcular o erro
        self.erroArredondamento = self.trapezios * vlArred * self.fatorAltura # Erro de arredondamento

        print("ERRO DE ARREDONDAMENTO: ")
        print(f"\n|Ea| <= {self.trapezios} * {vlArred:.{self.casasDecimais+1}f} * {self.fatorAltura:.{self.casasDecimais}f} <= |{self.erroArredondamento:.{self.casasDecimais+1}f}|\n")

    def calcErroTruncamento(self):
        # Esta função é para calcular o erro de truncamento, mas ainda não foi implementada
        valor = self.calcularMaxSegundaDerivada(self.expr, self.intervaloInicio, self.intervaloFim)
        a = self.intervaloInicio
        b = self.intervaloInicio + self.fatorAltura
        self.erroTruncamento = (((b-a)**3 / 12) * valor) * self.trapezios
        print(f"\nERRO DE TRUNCAMENTO:\n|Etru| <= ((({b} - {a})^3)/12) * {valor} * {self.trapezios} = {self.erroTruncamento:.{self.casasDecimais+1}f}\n")
    
    def calcErroTotal(self):
        erro_total = self.erroArredondamento + self.erroTruncamento
        print(f"\nERRO TOTAL: \n|Etotal| <= |Ea| + |Etru| < {self.erroArredondamento:.{self.casasDecimais+1}f} + {self.erroTruncamento:.{self.casasDecimais+1}f} = {erro_total:.{self.casasDecimais+1}f}\n")
    
    def intervalos(self):
        print("INTERVALO DA RESPOSTA:")
        print(f"\n{self.calculo:.{self.casasDecimais}f} - {self.erroArredondamento:.{self.casasDecimais+1}f} <= I <= {self.calculo:.{self.casasDecimais}f} + {self.erroArredondamento:.{self.casasDecimais+1}f}\n")
        print(f"Representação em colchetes: [{self.calculo - self.erroArredondamento:.{self.casasDecimais}f}; {self.calculo + self.erroArredondamento:.{self.casasDecimais}f}]\n")
        print(f"Representação em parênteses: ({self.calculo:.{self.casasDecimais}f}+-{self.erroArredondamento:.{self.casasDecimais+1}f})\n")

    def saida(self):
        self.criarTabela()

        print("\nSOMA DAS ÁREAS DOS TRAPÉZIOS: ")
        self.calcSomaErroIntervalo()

        self.calcErroTruncamento()
        self.calcErroTotal()
        self.intervalos()

CalcErroArredondamento()