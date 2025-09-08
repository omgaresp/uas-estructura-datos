// Crear tipo definido / Clase
class Persona {
    final private String nombre, apellido1, apellido2;
    
    public Persona(String nombre, String apellido1, String apellido2) {
        this.nombre = nombre;
        this.apellido1 = apellido1;
        this.apellido2 = apellido2;
    }
    
    @Override
    public String toString() {
        return nombre + " " + apellido1 + " " + apellido2;
    }
}

// Utilizarlo en un Array
public class Ejercicio2 {
    public static void main(String[] args) {
        Persona[] personas = {
            new Persona("Juan", "García", "López"),
            new Persona("María", "Rodríguez", "Martín"),
            new Persona("Carlos", "Hernández", "Pérez")
        };
        
        // Mostrar el array
        System.out.println("Array de Personas:");
        for (int i = 0; i < personas.length; i++) {
            System.out.println("[" + i + "]: " + personas[i]);
        }
    }
}