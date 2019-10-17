import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Panel;
import java.awt.RenderingHints;

public class TextPanel
  extends Panel
{
  Font bigfont = new Font("Monaco", 1, 25);
  Font smallfont = new Font("Monaco", 1, 15);
  int TOP_MARGIN = 35;
  int SIDE_MARGIN = 30;
  int LINE_HEIGHT = 50;
  int SPACING = 20;
  int[] PASTGUESSES;
  String QUOTE;
  
  public TextPanel()
  {
    setBackground(Color.cyan);
  }
  
  public void update(Graphics paramGraphics)
  {
    paint(paramGraphics);
  }
  
  public void newQuote(String paramString)
  {
    this.QUOTE = paramString;
    this.PASTGUESSES = new int[this.QUOTE.length()];
    repaint();
  }
  
  public void paint(Graphics paramGraphics)
  {
    Graphics2D localGraphics2D = (Graphics2D)paramGraphics;
    localGraphics2D.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
    
    int j = 0;
    int k = this.SIDE_MARGIN;
    int m = this.TOP_MARGIN;
    int n = getSize().width;
    int i1 = getSize().height;
    
    localGraphics2D.setColor(getBackground());
    localGraphics2D.fillRect(0, 0, n, i1);
    localGraphics2D.setColor(Color.black);
    localGraphics2D.drawRect(0, 0, n - 1, i1 - 1);
    for (int i2 = 0; i2 < this.QUOTE.length(); i2++)
    {
      if (k > n - this.SIDE_MARGIN)
      {
        k = this.SIDE_MARGIN;
        m += this.LINE_HEIGHT;
      }
      String str1 = "-";
      String str2 = "-";
      if (i2 < Entropy.POSITION)
      {
        str1 = this.QUOTE.substring(i2, i2 + 1);
        str2 = Integer.toString(this.PASTGUESSES[i2]);
      }
      else if (i2 == Entropy.POSITION)
      {
        str2 = "" + Entropy.CURRENTGUESS;
      }
      localGraphics2D.setFont(this.bigfont);
      int i = localGraphics2D.getFontMetrics().stringWidth(str1);
      localGraphics2D.drawString(str1, k - i / 2, m);
      localGraphics2D.setFont(this.smallfont);
      i = localGraphics2D.getFontMetrics().stringWidth(str2);
      localGraphics2D.drawString(str2, k - i / 2, m + 20);
      
      k += this.SPACING;
    }
  }
}
