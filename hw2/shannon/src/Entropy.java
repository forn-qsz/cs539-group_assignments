import java.applet.Applet;
import java.applet.AudioClip;
import java.awt.BorderLayout;
import java.awt.Button;
import java.awt.CardLayout;
import java.awt.Checkbox;
import java.awt.CheckboxGroup;
import java.awt.Color;
import java.awt.Font;
import java.awt.Label;
import java.awt.Panel;
import java.awt.TextArea;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.AdjustmentEvent;
import java.awt.event.AdjustmentListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.net.URL;
import java.util.Calendar;
import java.util.Random;

//import java.awt.*;
import java.awt.event.*;
import javax.swing.Timer;

import java.util.List;
import java.util.Arrays;

public class Entropy
  extends Applet
{
    Timer clock;
  String[] quotes;
  String[] demoquotes;
  final int WIDTH = 500;
  final int HEIGHT = 300;
  double[] stats;
  static int POSITION;
  static int CURRENTGUESS;
    static float ENTROPY; // upperbound
    static float ENTROPY_low; //lowerbound
  static String QUOTE;
  String CURRENTCARD;
  Random spin;
  Button entropy_button;
  Button newquote;
  Button okay;
  Button rand;
  Button dont;
  Checkbox on;
  Checkbox off;
  CheckboxGroup cbg;
  AudioClip smart;
  AudioClip any;
  AudioClip[] right_sounds;
  AudioClip[] wrong_sounds;
  LetterPanel letterpanel;
    TextPanel textpanel;
  TextArea textarea;
  boolean FINISHED;
  Panel cards;
  int[] wrong_sounds_list;
  int[] right_sounds_list;
  int wrong_position;
  int right_position;
    char LASTCHAR = ' ';
  
    javax.swing.Timer flipTimer;

  public Entropy()
  {
    this.quotes = new String[] { "SINCE THE LESSONS ARE FREE IF KNITTING DOESNT APPEAL TO YOU THEN YOU MIGHT WANT TO LEARN TO WATERSKI", 
				 "EVEN THOUGH YOU DONT KNOW HOW TO FLY YOU MIGHT BE ABLE TO LIFT YOUR SHOE LONG ENOUGH FOR THE CAT TO MOVE OUT FROM UNDERNEATH YOUR FOOT", 
				 "IT POURED EVERY TUESDAY OVER THE RECREATION CENTER WHEN THE INDIAN RAIN DANCE INSTRUCTOR TAUGHT HIS CLASS", 
				 "THE ONLY REASON THAT I MANAGED TO SURVIVE THE ACCIDENT WITHOUT MY HELMET IS THAT I SPENT YEARS DEVELOPING A TOLERANCE FOR BLOWS TO THE HEAD", 
				 "UNDERNEATH THE BLUE CUSHION IN THE LIVING ROOM IS A HANDFULL OF CHANGE AND THE REMOTE CONTROL", 
				 "BROWN BEAR WAS ALLOWED INTO THE CIRCUS TENT WITHOUT PAYING BECAUSE THE ATTENDANT WASNT WILLING TO ARGUE WITH ANYONE THAT HAD SUCH BIG TEETH", 
				 "MY PSYCHIC WOULD BE VERY INTERESTED TO LEARN HOW YOU MANAGED TO SWALLOW THAT EGG WHOLE WITHOUT BREAKING IT" };
    
    this.demoquotes = new String[] { "A MAN WHO CLEARS HIS THROAT WHEN HE EATS AND BLOWS HIS NOSE ON THE TABLECLOTH IS ILL BRED I ASSURE YOU" };
    
    //this.WIDTH = 500;
    //this.HEIGHT = 300;
    
    this.FINISHED = false;
  }
  
  public void init()
  {
    setBackground(new Color(250, 50, 50));
    setLayout(new BorderLayout());
    this.cbg = new CheckboxGroup();
    
    Panel localPanel1 = new Panel(new BorderLayout(15, 15));
    Panel localPanel2 = new Panel(new BorderLayout(15, 15));
    Panel localPanel3 = new Panel();
    localPanel3.add(this.letterpanel = new LetterPanel());
    Panel localPanel4 = new Panel();
    localPanel4.add(this.entropy_button = new Button("Entropy"));
    localPanel4.add(this.newquote = new Button("New Quote"));
    localPanel4.add(new Label("Audio:"));
    localPanel4.add(this.on = new Checkbox("On", this.cbg, true));
    localPanel4.add(this.off = new Checkbox("Off", this.cbg, false));
    localPanel2.add("Center", localPanel3);
    localPanel2.add("South", localPanel4);
    Panel localPanel5 = new Panel();
    localPanel5.setLayout(new BorderLayout());
    localPanel5.add("Center", this.textpanel = new TextPanel());
    localPanel1.add("Center", localPanel5);
    localPanel1.add("South", localPanel2);
    
    Panel localPanel6 = new Panel();
    localPanel6.setLayout(new BorderLayout(15, 15));
    localPanel6.add("Center", this.textarea = new TextArea("", 1, 1, 1));
    this.textarea.setFont(new Font("Helvetica", 1, 20));
    Panel localPanel7 = new Panel();
    localPanel7.add(this.rand = new Button("Random Quote"));
    localPanel7.add(this.okay = new Button("Accept"));
    localPanel7.add(this.dont = new Button("Cancel"));
    localPanel6.add("South", localPanel7);
    
    this.cards = new Panel();
    this.cards.setLayout(new CardLayout(15, 15));
    this.cards.add("EXPERIMENT", localPanel1);
    this.cards.add("NEWTEXT", localPanel6);
    add("Center", this.cards);
    
    this.stats = new double[28]; // for lowerbound
    for (int i = 0; i < 28; i++) {
      this.stats[i] = 0.0D;
    }
    this.spin = new Random(getranseed());
    QUOTE = this.quotes[((int)(this.quotes.length * this.spin.nextDouble()))];
    this.textpanel.newQuote(QUOTE);
    this.textarea.setText(QUOTE);
    POSITION = 0;
    CURRENTGUESS = 0;
    
    Entropy.Action localAction = new Entropy.Action();
    this.entropy_button.addActionListener(localAction);
    this.newquote.addActionListener(localAction);
    this.okay.addActionListener(localAction);
    this.rand.addActionListener(localAction);
    this.dont.addActionListener(localAction);
    this.textpanel.addKeyListener(localAction);
    this.textpanel.requestFocus();
    
    showCard("EXPERIMENT");

    this.LASTCHAR = ' ';
    
    loadSounds("sound"); // do not load 
    if (true) while (!this.FINISHED) {	
	    handleKey('2'); // bigram
	if (!this.FINISHED && this.CURRENTGUESS == 0) {
	    this.letterpanel.reset(); // reset unused_chars
	}
    }
    loadSounds("sounds");
  }
  
  public void start() {}
  
  public void stop() {}
  
  public void kill() {}
  
  public void destroy() {}
  
  public void loadSounds(String loadstr)
  {
      try {
	  URL localURL = getCodeBase();

	      
    String[] arrayOfString1 = { "allright", "bigbrain", "chore", "clapping", "correct", "excellent1", "excellent2", "faboo", "flanders", "force", "getprize", "giddyup", "goodshow", "groovy", "ilikeit", "imeanwoohoo", "impressive", "jackpot", "knowitall", "notsostupid", "ohyeah1", "ohyeah2", "outstanding", "savetheday", "smartest", "thatiscorrect", "thatsbetter1", "thatsbetter2", "thatsright", "woohoo", "yeahbaby", "yes", "youareright" };
    
    this.right_sounds = new AudioClip[arrayOfString1.length];
    for (int i = 0; i < arrayOfString1.length; i++) {
      this.right_sounds[i] = getAudioClip(localURL, loadstr + "/right/" + arrayOfString1[i] + ".au");
    }
    this.right_sounds_list = new int[3 * this.right_sounds.length / 4];
    this.right_position = 0;


    
    String[] arrayOfString2 = { "allwrong", "badfeeling", "bah", "bart", "beeguy", "boring", "cantbelieve", "canttakeit", "comefrom", "crazy", "dispicable", "doesnotcompute", "doh", "dumber", "extraordinarily", "failedme", "force", "gooddaysir", "haha", "holycow", "houston", "idjit", "illogical", "inconceivable", "insanelyidiotic", "insanity", "knownothing", "livinginavan", "loser", "loveofgod", "meathead", "next", "nicegirl", "no", "nobrain", "nosoup", "not", "ohbrother", "pathetic", "problem", "revolting", "seetobelieve", "shallnotpass", "shutyapper", "slappy1", "slappy2", "smartman", "sostupid", "spock", "strongox", "stupid", "stupidfathobbit", "stupidhead", "sucatash", "surely", "thinkmcfly", "thinkso", "weakestlink", "what", "whatsgoingon", "wideworld", "wrong", "yipe", "yosemite", "youfailed", "youstink" };
    
    this.wrong_sounds = new AudioClip[arrayOfString2.length];
    for (int j = 0; j < arrayOfString2.length; j++) {
      this.wrong_sounds[j] = getAudioClip(localURL, loadstr + "/wrong/" + arrayOfString2[j] + ".au");
    }
    this.wrong_sounds_list = new int[3 * this.wrong_sounds.length / 4];
    this.wrong_position = 0;
    
    this.smart = getAudioClip(localURL, loadstr + "/smart.au");
    this.any = getAudioClip(localURL, loadstr + "/anykey.au");
    this.any.play();
      } catch (Exception e) {
	  System.out.println("bad");
      }

  }
  
  public boolean isIn(int paramInt, int[] paramArrayOfInt)
  {
    boolean bool = false;
    int i = 0;
    while ((!bool) && (i < paramArrayOfInt.length))
    {
      if (paramArrayOfInt[i] == paramInt) {
        bool = true;
      }
      i++;
    }
    return bool;
  }
  
  public void handleKey(char paramChar)
  {
      // Penn Treebank unigram distribution
      double[] probs = {0.186707, 0.096553, 0.071996, 0.068170, 0.060494, 0.060356, 0.058854, 0.057930, 0.055399, 0.034810, 0.033429, 0.030767, 0.028639, 0.022293, 0.021886, 0.018266, 0.017698, 0.016187, 0.013612, 0.013483, 0.012018, 0.008218, 0.006514, 0.002186, 0.001680, 0.001116, 0.000738};

      //String unigram = " ETOAISHNRLDUMYWCFGBPVKJQXZ"; // Shakespear
      String unigram = " ETAIONSRLHDCUMPFGBYWVKXJQZ"; // Penn Treebank

      // Shakespear
      String[] bigram = {"TASHIMWBOFCLDYNPGERUKVJQZX", //  
			 "NTRLS YVIDMCKGUPBWFEJHZXQAO", // A
			 "EULORAYISTB JHDMWNGKV", // B
			 "OEHAKLTIURYC BQDSMN", // C
			 " EOISARUYLGDWNVMFKCHPTJB", // D
			 " RNSALDETMCVIYPFWXGOUBHKQZJ", // E
			 " OAERIFULTYSPNW", // F
			 " EHORAILUSNGBMTDYFPW", // G
			 "EAIO YTURNSMLBFWDCHQPV", // H
			 "NST LRMECOGDFVAUKPBZIXQWH", // I
			 "UOEAI", // J
			 "E INSLAOYFWRUMBHTCDP", // K
			 "L EOIADYSUFTKVCPMBRWNGZHQ", // L
			 "EAY OIUPBSMNLFWTRVCG", // M
			 "D OGETCSIAKYNRFULVJQWMHZBPX", // N
			 "UR NFTWMOLSDVPKBICYAEGHXZJQ", // O
			 "EROALI UPHTSYWBCKFMDN", // P
			 "U", // Q
			 " EOIADSTYURNMCLKGVFPBWHJQZ", // R
			 " TEHOISAUPWCLMYBKDNFGQRJV", // S
			 "H OEIARUSTYLWCNMFZJPBGDV", // T
			 "RS TLNCEGPMIDBKAFOYXZVUJ", // U
			 "EIAOYURLH", // V
			 "IHEAO NSRLDFBTYKMCGUPZ", // W
			 "TCEP AIFHUQOYLSM", // X
			 " OESIRAMLPCBTNFWZDHGVXK", // Y
			 "EAOZIYL WUV"}; // Z 
      /*
	// Penn Treebank
      String[] bigram = {"TASIOCBMWPFHRDENLGUYJVKQZX",  // ' '
			 "NRTLS ICDYGMBPVKUFWXJEZHAQO", // A
			 "EUOAILYRST BMJCVPNDWHFGK",    // B
			 "OEHATIKULR CYSQBDNMGFZPWVX",  // C
			 " EIAOUSRDYGLVMWNJCTFQHBPZK",  // D
			 " RSNDACLTEMXVPWIFYGOKBQUHZJ", // E
			 " OIREFAUTLSYCMKDBHGNPXZ",     // F
			 " EHRAOIUSNLGYTMDFBPKWJZ",     // G
			 "EA IOTRUSNYLMQWDBKFVCHPG",    // H
			 "NTSOCLDERAGVMF PBZKXUQIWJHY", // I
			 "UOAEIR SNCMPHKF",             // J
			 "E ISNAOLYRUHKFWBDTMPGZCVJ",   // K
			 " LIEAYODSUTRFVPMKCWBNGZHJXQ", // L
			 "EAIO PRMSBUYCNFLGDTHWKVX",    // M
			 " GDTESCAIOYKVUNFLMWHBRZJPQX", // N
			 "NR FUMSLWTPVCODIBAKGYEHJXZQ", // O
			 "REAOL PIUTHSMYCBFWGDJKNZVX",  // P
			 "U IVE",                       // Q
			 "E OAISTDNKYMRUGCLBPVFWHJZXQ", // R
			 " TEIASOHUPCLMKYWDFBNRQXVGZJ", // S
			 "H EOISARUTYLWMCNGFDVZBPKJX",  // T
			 "TRSNLCEAPIGMDBY FOXZKVJHWUQ", // U
			 "EIAO YSRUCVLNDXTKBGFHMJ",     // V
			 "IEAH ONSRTLYDMCPBFKUGQW",     // W
			 "P ECTAIOUXHWYLQMFDBNRSV",     // X
			 " ESOIMNALPTCBWDRUZFGVHKQJX",  // Y
			 "EAI OZUYLHMWTBDKSVGNRXCFQP"}; // Z
      */

    if (!this.FINISHED)
    {
      int i;
      // lhuang
      if (paramChar == '0') {
	  // unigram: sampling from distribution
	  double random = this.spin.nextDouble();
	  double sum = 0;
	  for (int j = 0; j < 27; j++) {
	      sum += probs[j];
	      if (random <= sum) {
		  paramChar = unigram.charAt(j);
		  break;
	      }
	  }
      }
      else if (paramChar == '1') {
	  // unigram: always choose the most probable
	  paramChar = unigram.charAt(CURRENTGUESS);
      }
      else if (paramChar == '2') {
	  // bigram
	  int id = LASTCHAR == ' ' ? 0 : (LASTCHAR - 'A' + 1);
	  paramChar = bigram[id].charAt(CURRENTGUESS);
      }
      else { 
	  // 0-gram
      int random = this.spin.nextInt(27);
      if (random == 26)
	  paramChar = ' ';
      else
	  paramChar = (char)(random + 65);
      }
      System.out.println("random guess: " + paramChar);

      if (paramChar == QUOTE.charAt(POSITION)) // correct guess
      {
	  LASTCHAR = paramChar;

	  //System.out.println("CORRECT! wrong guesses: " + CURRENTGUESS);
        this.textpanel.PASTGUESSES[POSITION] = (CURRENTGUESS + 1);
        this.stats[CURRENTGUESS] += 1.0D;
        if (POSITION < QUOTE.length() - 1)
        {
          if (this.cbg.getSelectedCheckbox() == this.on)
          {
            i = (int)(this.right_sounds.length * this.spin.nextDouble());
            while (isIn(i, this.right_sounds_list)) {
              i = (int)(this.right_sounds.length * this.spin.nextDouble());
            }
            this.right_sounds_list[(this.right_position++)] = i;
            if (this.right_position == this.right_sounds_list.length) {
              this.right_position = 0;
            }
            if (this.right_sounds[i] != null) 
		this.right_sounds[i].play();
          }
        }
        else
        {
          this.FINISHED = true;
          this.letterpanel.MODE = 1;
          this.entropy_button.setLabel("Letters");
          if (this.cbg.getSelectedCheckbox() == this.on) {
	      if (this.smart != null)
		  this.smart.play();
          }
        }
        POSITION += 1;
        CURRENTGUESS = 0;
        ENTROPY = getEntropy();
	ENTROPY_low = getEntropy_low();
      }
      else if (this.letterpanel.guessLetter(paramChar)) // new wrong guess (previously uncovered guess)
      {
	  //System.out.println("WRONG GUESS! current guess: " + CURRENTGUESS);
        CURRENTGUESS += 1;
        if (this.cbg.getSelectedCheckbox() == this.on)
        {
          i = (int)(this.wrong_sounds.length * this.spin.nextDouble());
          while (isIn(i, this.wrong_sounds_list)) {
            i = (int)(this.wrong_sounds.length * this.spin.nextDouble());
          }
          this.wrong_sounds_list[(this.wrong_position++)] = i;
          if (this.wrong_position == this.wrong_sounds_list.length) {
            this.wrong_position = 0;
          }
	  if (this.wrong_sounds[i] != null)
	      this.wrong_sounds[i].play();
        }
      }
    }
    this.letterpanel.repaint(); // also renew unused_chars
    this.textpanel.repaint();
  }
  
  public void showCard(String paramString)
  {
    this.CURRENTCARD = paramString;
    ((CardLayout)this.cards.getLayout()).show(this.cards, paramString);
  }
  
  public String randQuote()
  {
    return this.quotes[((int)(this.quotes.length * this.spin.nextDouble()))];
  }
  
  public void newQuote(String paramString)
  {
    this.textpanel.newQuote(paramString);
    QUOTE = paramString;
    for (int i = 0; i < 28; i++) {
      this.stats[i] = 0.0D;
    }
    this.letterpanel.reset();
    this.FINISHED = false;
    POSITION = 0;
    CURRENTGUESS = 0;
    this.textpanel.repaint();
    this.textarea.setText(QUOTE);
  }
  
  public void acceptQuote()
  {
    QUOTE = "";
    String str = this.textarea.getText().toUpperCase();
    for (int i = 0; i < str.length(); i++)
    {
      char c = str.charAt(i);
      if ((Character.isLetter(c)) || (c == ' ')) {
        QUOTE += c;
      }
    }
    newQuote(QUOTE);
    showCard("EXPERIMENT");
  }
  
  public void switchMode()
  {
    if (this.entropy_button.getLabel().equals("Entropy"))
    {
      if (POSITION > 0)
      {
        ENTROPY = getEntropy();
	ENTROPY_low = getEntropy_low();

        this.letterpanel.MODE = 1;
        this.letterpanel.repaint();
        this.entropy_button.setLabel("Letters");
      }
    }
    else
    {
      this.letterpanel.MODE = 0;
      this.letterpanel.repaint();
      this.entropy_button.setLabel("Entropy");
    }
  }
  
  public float getEntropy()
  {
    double d1 = 0.0D;
    System.out.println("POSITION = " + POSITION);
    for (int i = 0; i < 27; i++) {
      if (this.stats[i] > 0.0D)
      {
	  // entropy of language is upperbounded by entropy of guesses
	  System.out.println(i + " wrong guesses: " + this.stats[i] + " times");
        double d2 = this.stats[i] / POSITION;
        d1 -= d2 * Math.log(d2);
      }
    }
    return (float)(d1 / Math.log(2.0D));
  }
  
  public float getEntropy_low()
  {
    double d1 = 0.0D;
    System.out.println("POSITION = " + POSITION);
    for (int i = 0; i < 27; i++) {
	//if (this.stats[i] > 0.0D)
      {
	  //System.out.println(i + " wrong guesses: " + this.stats[i] + " times");
	  double d3 = (this.stats[i] - this.stats[i+1]) / POSITION;
	  d1 += (i+1) * d3 * Math.log(i+1);
      }
    }
    return (float)(d1 / Math.log(2.0D));
  }

  private long getranseed()
  {
    Calendar localCalendar = Calendar.getInstance();
    return Math.round(Math.abs(Math.sin(localCalendar.get(13) * localCalendar.get(12))) * 2.1942134E7D);
  }

  class Action
    implements AdjustmentListener, ActionListener, KeyListener
  {
    Action() {}
    
    public void adjustmentValueChanged(AdjustmentEvent paramAdjustmentEvent)
    {
      Entropy.this.textpanel.requestFocus();
    }
    
    public void actionPerformed(ActionEvent paramActionEvent)
    {
      Object localObject = paramActionEvent.getSource();
      if (localObject == Entropy.this.newquote) {
        Entropy.this.newQuote(Entropy.this.randQuote());
      } else if (localObject == Entropy.this.entropy_button) {
        Entropy.this.switchMode();
      } else if (localObject == Entropy.this.okay) {
        Entropy.this.acceptQuote();
      } else if (localObject == Entropy.this.rand) {
        Entropy.this.textarea.setText(Entropy.this.randQuote());
      } else if (localObject == Entropy.this.dont) {
        Entropy.this.showCard("EXPERIMENT");
      }
      Entropy.this.textpanel.requestFocus();
    }
    
    public void keyTyped(KeyEvent paramKeyEvent)
    {
      char c = paramKeyEvent.getKeyChar();
      if (c == ' ') {
        Entropy.this.handleKey(c);
      } else if (c == '\016') {
        Entropy.this.showCard("NEWTEXT");
      } else if (Character.isLetter(c)) {
        Entropy.this.handleKey(Character.toUpperCase(c));
      }
    }
    
    public void keyReleased(KeyEvent paramKeyEvent) {}
    
    public void keyPressed(KeyEvent paramKeyEvent) {}
  }
}
