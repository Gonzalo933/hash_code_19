import java.io.File;
import java.io.IOException;

/**
 * Clase que contiene el metodo Main del programa
 * Filtra los argumentos introducidos al invocar dicho metodo
 * Controla el orden de ejecucion del programa
 *
 * @author Juan Francisco Casanova Ferrer
 * teléfono: 625803490
 * email:    juancasanovaferrer@gmail.com
 * Google Hash Code
 */
class Pizza {
    private boolean help = false;
    private String archivoEntrada = null;

    /**
     * @param argumentos Argumentos pasados por el usuario al iniciar el programa
     */
    private Pizza(String[] argumentos) throws IOException {

        // Filtracion de los argumentos
        filtrar(argumentos);

        // Ejecucion del programa
        ejecutar();
    }

    /**
     * Metodo Main del programa
     *
     * @param args Argumentos de entrada
     * @throws IOException Si no se encuentra el archivo de entrada especificado
     */
    public static void main(String[] args) throws IOException {
        new Pizza(args);
    }

    /**
     * Filtra los argumentos y los asigna a las variables correspondientes
     *
     * @param argumentos Argumentos de entrada
     */
    private void filtrar(String[] argumentos) {
        for (String argumento : argumentos) {
            if (argumento.equals("-h")) {
                help = true;
            } else {
                archivoEntrada = argumento;
            }
        }
    }

    /**
     * Controlador del programa
     *
     * @throws IOException Si no se localiza el archivo de entrada
     */
    private void ejecutar() throws IOException {

        // Si se desea mostrar la ayuda, se muestra y termina la ejecucion
        if (help) {
            Impresor.imprimirHelp();
            System.exit(0);
        }

        // El interprete parsea los datos del archivo de entrada
        Interprete interprete = setInterprete();

        // El algoritmo realiza las operaciones y las guarda en su variable de instancia solucion
        Algoritmo algoritmo = new Algoritmo(interprete);

        // Se guardan los resultados en el archivo de salida
        Impresor.archivoSalida(archivoEntrada, algoritmo.getSolucion());
    }

    /**
     * Crea un interprete para datos a traves de la consola o a traves de un archivo
     *
     * @return Interprete de datos de entrada
     * @throws IOException Si no se encuentra el archivo de entrada especificado
     */
    private Interprete setInterprete() throws IOException {
        if (archivoEntrada == null || !new File(archivoEntrada).exists()) {
            System.out.println();
            System.err.println("No se ha encontrado el archivo de entrada. El programa se va a cerrar");
            System.exit(0);
        }
        return new Interprete(archivoEntrada);
    }
}