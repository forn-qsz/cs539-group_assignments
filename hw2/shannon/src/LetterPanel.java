import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Panel;
import java.awt.RenderingHints;
import javax.swing.Timer; // lhuang
import java.awt.event.ActionListener; // lhuang
import java.awt.event.ActionEvent; // lhuang

public class LetterPanel
  extends Panel
{
  int SIZE = 18;
  Font font = new Font("Helvetica", 1, this.SIZE);
  String UNUSED_LETTERS;
  int MODE;
  
  public LetterPanel()
  {
    setBackground(Color.orange);
    reset();
  }
  
  public Dimension minimumSize()
  {
    return preferredSize();
  }
  
  public Dimension preferredSize()
  {
    return new Dimension(540, 40);
  }
  
  public void reset()
  {
    this.UNUSED_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    this.MODE = 0;
    repaint();

  }
  
  public boolean guessLetter(char paramChar)
  {
      //System.out.println("guessed " + paramChar + " unused: " + this.UNUSED_LETTERS);
    if (paramChar == ' ')
    {
      if (this.UNUSED_LETTERS.charAt(26) == ' ')
      {
        this.UNUSED_LETTERS = this.UNUSED_LETTERS.replace(' ', '*');
        this.MODE = 0;
        repaint();
        return true;
      }
    }
    else if (this.UNUSED_LETTERS.charAt(paramChar - 'A') == paramChar)
    {
      this.UNUSED_LETTERS = this.UNUSED_LETTERS.replace(paramChar, '*');
      this.MODE = 0;
      repaint();
      return true;
    }
    return false;
  }
  
  public void update(Graphics paramGraphics)
  {
    paint(paramGraphics);
  }
  
  public void paint(Graphics paramGraphics)
  {
    Graphics2D localGraphics2D = (Graphics2D)paramGraphics;
    localGraphics2D.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
    
    int j = getSize().width;
    int k = getSize().height;
    
    localGraphics2D.setFont(this.font);
    localGraphics2D.setColor(getBackground());
    localGraphics2D.fillRect(0, 0, j, k);
    localGraphics2D.setColor(Color.black);
    localGraphics2D.drawRect(0, 0, j - 1, k - 1);

    if (Entropy.CURRENTGUESS == 0) {
      this.UNUSED_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";
    }
    String str;
    int i;
    if (this.MODE == 0)
    {
      localGraphics2D.setColor(Color.blue);
      for (int m = 1; m < 27; m++)
      {
        str = this.UNUSED_LETTERS.substring(m - 1, m);
        i = localGraphics2D.getFontMetrics().stringWidth(str);
        if (!str.equals("*")) {
          localGraphics2D.drawString(str, (this.SIZE - 1) * m - i / 2, k - 15);
        }
      }
      if (this.UNUSED_LETTERS.charAt(26) == ' ') {
        localGraphics2D.drawString("SPACE", (this.SIZE - 1) * 27, k - 15);
      }
    }
    else
    {
      str = "The entropy for this experiment is in [" + Entropy.ENTROPY_low + ", " + Entropy.ENTROPY + "]";
      i = localGraphics2D.getFontMetrics().stringWidth(str);
      localGraphics2D.setColor(Color.black);
      localGraphics2D.drawString(str, (j - i) / 2, k - 15);
    }
  }
}
