import java.awt.Robot;
import java.awt.event.KeyEvent;

public class CS_4632_W01_Windbigler_04_test{
    public static void main(String[] args) throws Exception {
        Robot robot = new Robot();
        
        // Simulate a key press (example: press and release 'A')
        robot.keyPress(KeyEvent.VK_A);
        robot.keyRelease(KeyEvent.VK_A);
        
        // Simulate a mouse click at (x=500, y=500)
        robot.mouseMove(500, 500);
        robot.mousePress(KeyEvent.BUTTON1_MASK);
        robot.mouseRelease(KeyEvent.BUTTON1_MASK);
    }
}
