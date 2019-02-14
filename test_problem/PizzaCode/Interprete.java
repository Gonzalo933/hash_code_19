import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

/**
 * Interprete de los datos albergados en el fichero de entrada
 *
 * @author Juan Francisco Casanova Ferrer
 * teléfono: 625803490
 * email:    juancasanovaferrer@gmail.com
 * Google Hash Code
 */
class Interprete {
    private int[][] pizza; // Matriz en la que guardamos la pizza
    private int r, c, l, h;

    /**
     * @param archivoEntrada Archivo en el que se encuentran los datos
     * @throws IOException En el caso de que no se encuentre el archivo
     */
    Interprete(String archivoEntrada) throws IOException {

        BufferedReader br = new BufferedReader(new FileReader(archivoEntrada));

        // Variable que va guardando la fila que parseamos del archivo
        String line;

        // Inicializamos r a 0 para poder empezar el bucle (vamos a parsear r+1 filas)
        r = 0;

        int i = 0;
        while ((line = br.readLine()) != null && i <= r) {

            // Leemos la primera linea del archivo de entrada y asignamos los valores a las variables correspondientes
            if (i == 0) {
                String[] datos = line.split(" ");
                r = Integer.parseInt(datos[0]);
                c = Integer.parseInt(datos[1]);
                l = Integer.parseInt(datos[2]);
                h = Integer.parseInt(datos[3]);

                pizza = new int[r][c];
            }

            // Creamos un string para guardar la fila de la pizza
            String[] fila = line.split(" ");

            // Asignamos los ingredientes correspondientes a cada fila de la matriz
            int j = 0;
            for (String ingrediente: fila) {
                switch (ingrediente) {
                    case "T":
                        pizza[i-1][j] = 0;
                        break;
                    case "M":
                        pizza[i-1][j] = 1;
                        break;
                }
                j++;
            }

            i++;
        }
    }

    // Getter pizza: devuelve la pizza
    int[][] getPizza() {
        return pizza;
    }

    // Getter r: número de filas de la pizza
    int getR() {
        return r;
    }

    // Getter m: número de columnas de la pizza
    int getC() {
        return c;
    }

    // Getter l: número mínimo de cada ingrediente por trozo de la solución
    int getL() {
        return l;
    }

    // Getter h: número máximo de celdas en cada trozo de la solucion
    int getH() {
        return h;
    }
}
