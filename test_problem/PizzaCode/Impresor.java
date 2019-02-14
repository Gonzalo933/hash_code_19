import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

/**
 * Encargado de crear un archivo de salida o de mostrar la ayuda en pantalla
 *
 * @author Juan Francisco Casanova Ferrer
 * teléfono: 625803490
 * email:    juancasanovaferrer@gmail.com
 * Google Hash Code
 */
final class Impresor {

    /**
     * Muestra una ayuda y la sintaxis del comando
     */
    static void imprimirHelp() {
        System.out.println();
        System.out.println("_______________________________________________________________________");
        System.out.println("DESCRIPCION:");
        System.out.println("Práctica de la Pizza");
        System.out.println("_______________________________________________________________________");
        System.out.println("SINTAXIS:");
        System.out.println("java suma [-h] [fichero_entrada]");
        System.out.println("o");
        System.out.println("java –jar suma.jar [-h] [fichero_entrada]");
        System.out.println("_______________________________________________________________________");
        System.out.println("ARGUMENTOS:");
        System.out.println("-h                          Muestra esta ayuda");
        System.out.println("fichero_entrada             Nombre del fichero de entrada");
        System.out.println("_______________________________________________________________________");
        System.out.println("FORMATO ENTRADA:");
        System.out.println("El descrito en el PDF ");
        System.out.println("___________________________________________________________");
        System.out.println("AUTOR: Juan Francisco Casanova Ferrer");
        System.out.println("Google Hash Code");
        System.out.println("Pizza");
        System.out.println();
    }

    /**
     * Genera un archivo que contiene los datos de la solucion
     *
     * @param archivoSalida Archivo donde se almacenara la solucion
     * @param solucion      Guarda la solución
     */
    static void archivoSalida(String archivoSalida, List<int[]> solucion) throws IOException {

        // Obtenemos el número de milisegundos desde el UNIX epoch
        String milisegundos = String.valueOf(System.currentTimeMillis());

        // Concatenamos los milisegundos al nombre del archivo de salida (que es el mismo que el de entrada)
        // para obtener un nombre de salida único con cada ejecución y así no tener problemas
        archivoSalida = archivoSalida.concat("_").concat(milisegundos);

        // Creamos una variable que almacenará los datos a escribir en el archivo
        ArrayList<String> filas = new ArrayList<>();

        // Añadimos cada entrada de la solucion a la variable anterior. Para ello hay que pasarlo a String
        for (int[] linea : solucion) {
            StringBuilder fila = new StringBuilder();
            for (Integer numero : linea) {
                fila.append(numero).append(" ");
            }
            filas.add(fila.toString().trim());
        }

        Path file = Paths.get(archivoSalida);
        Files.write(file, filas, Charset.forName("UTF-8"));
    }
}
