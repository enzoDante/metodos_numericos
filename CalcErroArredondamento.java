import javax.swing.JOptionPane;

public class CalcErroArredondamento {

    private double vlInicial;
    private double vlFinal;
    private int qtdCasasDec;
    private int numTrap;
    private double area;
    private double altura;
    private double fatorAltura;
    private double calculo;
    private boolean tabelaCriada = false;
    private boolean calcErro = false;
    private String tabela;
    private String entrada;
    
    public CalcErroArredondamento() {
        receberDadosdoProblema();
        calculoTrap();
        menu();
    }

    public void receberDadosdoProblema() {
        try {
            entrada = JOptionPane.showInputDialog("Digite o valor inicial do intervalo:");

            if (entrada == null) {
                JOptionPane.showMessageDialog(null, "PROGRAMA CANCELADO!");
                System.exit(0);
            }

            vlInicial = Double.parseDouble(entrada);

        }catch(NumberFormatException e){
            JOptionPane.showMessageDialog(null, "ERRO! DIGITE APENAS NÚMEROS!");
            System.exit(0);
        }
        try {
            entrada = JOptionPane.showInputDialog("Digite o valor final do intervalo:");

            if (entrada == null) {
                JOptionPane.showMessageDialog(null, "PROGRAMA CANCELADO!");
                System.exit(0);
            }

            vlFinal = Double.parseDouble(entrada);

        }catch(NumberFormatException e){
            JOptionPane.showMessageDialog(null, "ERRO! DIGITE APENAS NÚMEROS!");
            System.exit(0);
        }
        try {
            entrada = JOptionPane.showInputDialog("Digite a quantidade de trapézios:");

            if (entrada == null) {
                JOptionPane.showMessageDialog(null, "PROGRAMA CANCELADO!");
                System.exit(0);
            }

            numTrap = Integer.parseInt(entrada);

        }catch(NumberFormatException e){
            JOptionPane.showMessageDialog(null, "ERRO! DIGITE APENAS NÚMEROS!");
            System.exit(0);
        }
        try {
            entrada = JOptionPane.showInputDialog("Digite a quantidade de casas decimais desejada para as respostas");

            if (entrada == null) {
                JOptionPane.showMessageDialog(null, "PROGRAMA CANCELADO!");
                System.exit(0);
            }

            qtdCasasDec = Integer.parseInt(entrada);

        }catch(NumberFormatException e){
            JOptionPane.showMessageDialog(null, "ERRO! DIGITE APENAS NÚMEROS!");
            System.exit(0);
        }
    }
    
    public void calculoTrap() {
        altura = vlFinal - vlInicial;
        fatorAltura = altura / numTrap;
        JOptionPane.showMessageDialog(null,"A altura de cada Trapézio (eixo X) consiste na razão entre a diferença \ndos valores do intervalo e o número de trapézios declarado!");
    }

    public void criarTabela() {
        int i;
        double[] aux = new double[numTrap + 1];
        double[] raizQuad = new double[numTrap + 1];
        double soma;
        aux[0] = vlInicial;
        soma = 0;
        StringBuilder construirTabela = new StringBuilder();
        for(i=0;i<=numTrap;i++) {
            raizQuad[i] = Math.sqrt(aux[i]);
            if (i < numTrap) { aux[i + 1] = aux[i] + fatorAltura; } // Evita estouro
        }
        raizQuad[0] = raizQuad[0] / 2;
        raizQuad[numTrap] = raizQuad[numTrap] / 2;
        construirTabela.append("   X          f(X)\n");
        for(i=0;i<=numTrap;i++) {
            soma += raizQuad[i];
            construirTabela.append(String.format("%." + qtdCasasDec + "f    %." + qtdCasasDec + "f\n", aux[i], raizQuad[i]));
        }
        construirTabela.append("-------------------\n");
        construirTabela.append(String.format("            %." + qtdCasasDec + "f", soma));
        tabela = construirTabela.toString();
        tabelaCriada = true;
    }
    
    public void exibirTabela() {
        if (!tabelaCriada) {
            JOptionPane.showMessageDialog(null, "ERRO! A TABELA AINDA NÃO FOI CRIADA!");
            return;
        }
        JOptionPane.showMessageDialog(null, tabela);
    }
    
    public void calcErroArred() {
        int i, soma, ultimaCasa;
        double[] aux = new double[numTrap + 1];
        double[] raizQuad = new double[numTrap + 1];
        double vlArred, erroArredondamento;
        long temp;
        aux[0] = vlInicial;
        soma = 0;
        for(i=0;i<=numTrap;i++) {
            raizQuad[i] = Math.sqrt(aux[i]);
            if (i < numTrap) { aux[i + 1] = aux[i] + fatorAltura; }
        }
        for(i=0;i<numTrap;i++){
            calculo += ((raizQuad[i+1] + raizQuad[i]) / 2) * fatorAltura;
        }
        temp = Math.round(calculo * Math.pow(10, qtdCasasDec));
        ultimaCasa = (int)(temp % 10);
        vlArred = 0.5 * Math.pow(10, -qtdCasasDec);
        erroArredondamento = numTrap * vlArred * fatorAltura;
        calcErro = true;
        JOptionPane.showMessageDialog(null,String.format("|Ea| <= %d * %f * %f = %f", numTrap, vlArred, fatorAltura, erroArredondamento)); 
    }

    public void getNumTrap() {
        JOptionPane.showMessageDialog(null,String.format("Número de Trapézios = %d", numTrap)); 
    }
    
    public void getCasasDecimais() {
        JOptionPane.showMessageDialog(null,String.format("Número de Casas Decimais = %d", qtdCasasDec)); 
    }
    
    public void getAlturaCadaTrap() {
        JOptionPane.showMessageDialog(null,String.format("Altura de cada Trapézio = %f", fatorAltura)); 
    }

    public void getInicioIntervalo() {
        JOptionPane.showMessageDialog(null,String.format("Valor de início do intervalo = %f", vlInicial)); 
    }
    
    public void getFimIntervalo() {
        JOptionPane.showMessageDialog(null,String.format("Valor do fim do intervalo = %f", vlFinal)); 
    }
    
    public void getValorSomatorio() {
        if (!calcErro) {
            JOptionPane.showMessageDialog(null, "ERRO! A SOMATORIA AINDA NÃO FOI CALCULADA!");
            return;
        }
        JOptionPane.showMessageDialog(null,String.format("Resultado do Somatorio = %." + qtdCasasDec + "f", calculo)); 
    }
    
    public void menu() {
        int opcao = -1;
        do {
            try {
                
                entrada = JOptionPane.showInputDialog(
                "=== MENU ===\n" +
                "1 - Calcula Erro de Arredondamento\n" +
                "2 - Criar Tabela de 'x' e 'f(x)'\n" +
                "3 - Exibir Tabela\n" +
                "4 - Dados do Problema\n" +
                "0 - Sair\n\n" +
                "Escolha uma opção:"
                );
            
                if(entrada == null) {
                    JOptionPane.showMessageDialog(null, "PROGRAMA FINALIZADO!");
                    System.exit(0);
                }

                opcao = Integer.parseInt(entrada);

                switch(opcao) {
                    case 1 -> calcErroArred();
                    case 2 -> { 
                        criarTabela();
                        JOptionPane.showMessageDialog(null, "Tabela de valores criada e preenchida com sucesso!");
                    }
                    case 3 -> exibirTabela();
                    case 4 -> {
                        getInicioIntervalo();
                        getFimIntervalo();
                        getNumTrap();
                        getCasasDecimais();
                        getAlturaCadaTrap();
                        getValorSomatorio();
                    }
                    case 0 -> JOptionPane.showMessageDialog(null, "SAINDO DO PROGRAMA...");
                    default -> JOptionPane.showMessageDialog(null, "OPCAO INVALIDA!");
                }
            }catch(NumberFormatException e) {
                JOptionPane.showMessageDialog(null, "ERRO! DIGITE APENAS NÚMEROS!");
                System.exit(0);
            }
        } while(opcao != 0);
    }
    
    public static void main(String[] args) {
        new CalcErroArredondamento();
    }
}