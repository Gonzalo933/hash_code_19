import java.util.ArrayList;
import java.util.List;

/**
 * Clase que contiene el algoritmo que calcula el resultado del problema
 *
 * @author Juan Francisco Casanova Ferrer
 * teléfono: 625803490
 * email:    juancasanovaferrer@gmail.com
 * Google Hash Code
 */
class Algoritmo {
    // Lista que contiene la solución
    // La primera linea contiene el número de trozos
    // Las siguientes líneas contienen cuatro números que indican los límites de los trozos
    private List<int[]> solucion;

    /**
     * @param pizza Matriz que contiene el contenido de la pizza
     * @param r     Número de filas de la pizza
     * @param c     Número de columnas de la pizza
     * @param l     Número mínimo de cada ingrediente por trozo de la solución
     * @param h     Número máximo de celdas en cada trozo de la solucion
     */
    Algoritmo(int[][] pizza, int r, int c, int l, int h) {
        solucion = new ArrayList<>();

        // Inicio del calculo.
        calculo("parametros");
    }

    /**
     * Algoritmo que calcula la solucion
     */
    private void calculo(String parametros) {
        System.out.println("Aquí se hacen los cálculos y se añaden los datos a solucion");
    }

    // Getter solucion
    List<int[]> getSolucion() {
        return solucion;
    }
}