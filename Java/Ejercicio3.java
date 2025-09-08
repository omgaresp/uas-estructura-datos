import java.util.ArrayList;

public class Ejercicio3 {
    
    // Tipo definido Persona
    static class Persona {
        String nombre, apellido1, apellido2;
        
        Persona(String nombre, String apellido1, String apellido2) {
            this.nombre = nombre;
            this.apellido1 = apellido1;
            this.apellido2 = apellido2;
        }
    }
    
    public static void main(String[] args) {
        
        // ARRAY NORMAL
        System.out.println("=== ARRAY NORMAL ===");
        ArrayList<Integer> arrayNumeros = new ArrayList<>();
        arrayNumeros.add(11);
        arrayNumeros.add(12);
        arrayNumeros.add(13);
        arrayNumeros.add(14);
        arrayNumeros.add(15);
        
        System.out.println("Recorrido inicial:");
        for (int i = 0; i < arrayNumeros.size(); i++) {
            System.out.println("[" + i + "]: " + arrayNumeros.get(i));
        }
        
        // Buscar el 15
        System.out.println("\nBuscando el valor 15:");
        boolean encontrado = false;
        for (int i = 0; i < arrayNumeros.size(); i++) {
            if (arrayNumeros.get(i) == 15) {
                System.out.println("¡Encontrado! El valor 15 está en la posición " + i);
                encontrado = true;
                break;
            } else {
                System.out.println("Posición " + i + ": " + arrayNumeros.get(i) + " - No es 15");
            }
        }

        arrayNumeros.add(1, 18);
        
        System.out.println("\nRecorrido después de la inserción:");
        for (int i = 0; i < arrayNumeros.size(); i++) {
            if (arrayNumeros.get(i) == 18) {
                System.out.println("[" + i + "]: " + arrayNumeros.get(i) + " ← NUEVO ELEMENTO INSERTADO");
            } else {
                System.out.println("[" + i + "]: " + arrayNumeros.get(i));
            }
        }

        System.out.println("\nRecorrido inverso:");
            for (int i = arrayNumeros.size() - 1; i >= 0; i--) {
                System.out.println("[" + i + "]: " + arrayNumeros.get(i));
        }
        
        // ARRAY CON TIPO DEFINIDO
        System.out.println("\n=== ARRAY CON TIPO DEFINIDO ===");
        ArrayList<Persona> personas = new ArrayList<>();
        personas.add(new Persona("Juan", "García", "López"));
        personas.add(new Persona("María", "Rodríguez", "Martín"));
        personas.add(new Persona("Carlos", "Hernández", "Pérez"));
        
        System.out.println("Recorrido inicial:");
        for (int i = 0; i < personas.size(); i++) {
            Persona p = personas.get(i);
            System.out.println("[" + i + "]: " + p.nombre + " " + p.apellido1 + " " + p.apellido2);
        }
        
        // Buscar a Juan
        System.out.println("\nBuscando a Juan:");
        encontrado = false;
        for (int i = 0; i < personas.size(); i++) {
            if (personas.get(i).nombre.equals("Juan")) {
                System.out.println("¡Encontrado! Juan está en la posición " + i);
                encontrado = true;
                break;
            } else {
                System.out.println("Posición " + i + ": " + personas.get(i).nombre + " - No es Juan");
            }
        }
        
        personas.add(2, new Persona("Omar", "García", "Espinoza"));
        
        System.out.println("\nRecorrido después de la inserción:");
        for (int i = 0; i < personas.size(); i++) {
            Persona p = personas.get(i);
            if (p.nombre.equals("Omar")) {
                System.out.println("[" + i + "]: " + p.nombre + " " + p.apellido1 + " " + p.apellido2 + " ← NUEVA PERSONA INSERTADA");
            } else {
                System.out.println("[" + i + "]: " + p.nombre + " " + p.apellido1 + " " + p.apellido2);
            }
        }

        System.out.println("\nRecorrido inverso:");
        for (int i = personas.size() - 1; i >=0; i--) {
            Persona p = personas.get(i);
            System.out.println("[" + i + "]: " + p.nombre + " " + p.apellido1 + " " + p.apellido2);
        }
    }
}