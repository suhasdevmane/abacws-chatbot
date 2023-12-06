import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class TestJDBC {
    public static void main(String[] args) {
        String jdbcUrl = "jdbc:postgresql://localhost:5432/thingsboard";
        String username = "thingsboard";
        String password = "postgres";

        try {
            Connection connection = DriverManager.getConnection(jdbcUrl, username, password);
            System.out.println("JDBC connection established successfully.");
            connection.close();
        } catch (SQLException e) {
            System.err.println("Failed to connect to the database. Error: " + e.getMessage());
        }
    }
}
