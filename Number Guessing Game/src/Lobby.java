package src;

//All imports 
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.geom.RoundRectangle2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;
import javax.imageio.ImageIO;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.swing.ImageIcon;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.border.EmptyBorder;
import javax.swing.JLabel;
import java.awt.Color;
import java.awt.Font;
import java.awt.SystemColor;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

//Lobby Class
public class Lobby extends JFrame {
	// Declaration of static variables
	public static Random rand = new Random();
	public static int number;
	public static int count;
	public static Clip clip;
	public static String Syspath = System.getProperty("user.dir");
	public static Set<Clip> activeClips = new HashSet<>();

	private static final long serialVersionUID = 1L;
	private JPanel contentPane;

	public class BgPanel extends JPanel {
		private static final long serialVersionUID = 1L;

		@Override
		public void paintComponent(Graphics gr) {
			super.paintComponent(gr);
			Graphics2D g = (Graphics2D) gr;
			BufferedImage img = null;
			try {

				File file = new File(Syspath + File.separator + "Images\\bggood.png");
				img = ImageIO.read(file);
			} catch (IOException e) {
				e.printStackTrace();
			}
			g.drawImage(img, 0, 0, this.getWidth(), this.getHeight(), this);

		}
	}

	// PlaySound Function
	public static void playSound(String soundFilePath) {
		try {
			File soundFile = new File(soundFilePath);
			AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(soundFile);
			clip = AudioSystem.getClip();
			clip.open(audioInputStream);
			clip.start();

			activeClips.add(clip);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	// Method to stop all active sounds
	public static void stopAllSounds() {
		for (Clip clip : activeClips) {
			if (clip.isRunning()) {
				clip.stop();
			}
		}
		// Clear the set of active clips
		activeClips.clear();
	}


	// Main Function
	public static void main(String[] args) {
		System.out.println(Syspath);
		SwingUtilities.invokeLater(() -> {
			Lobby frame = new Lobby(); // Creation of new object of lobby class
			frame.setUndecorated(true);
			frame.setLocationRelativeTo(null);
			frame.setResizable(false);
			frame.setShape(new RoundRectangle2D.Double(0, 0, frame.getWidth(), frame.getHeight(), 20, 20));
			frame.setVisible(true);
			Image icon = new ImageIcon(Syspath + File.separator + "Images\\question.png").getImage();
			frame.setIconImage(icon);
		});

	}

	// Mechanics Function
	public static void mechanics(String Difficulty) {
		Thread mechanicsThread = new Thread(() -> {
			JFrame newframe = new JFrame();
			newframe.setUndecorated(true);
			newframe.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			newframe.setSize(838, 527);
			newframe.setLocationRelativeTo(null);

			JPanel newcontentPane = new JPanel();
			newframe.setContentPane(newcontentPane);
			newcontentPane.setLayout(null);

			JPanel panel2 = new JPanel();
			panel2.setBounds(0, 0, newframe.getWidth(), newframe.getHeight());
			panel2.setBackground(Color.BLACK);
			panel2.setLayout(null);
			newcontentPane.add(panel2);

			// ProgressBar for number of attempts
			JProgressBar progressBar = new JProgressBar();
			progressBar.setBorderPainted(false);
			progressBar.setBorder(null);
			progressBar.setForeground(Color.GREEN);
			progressBar.setValue(count);
			progressBar.setBounds(0, 310, panel2.getWidth(), 8);
			panel2.add(progressBar);

			// Label for LowerLimit
			JLabel greaterThan = new JLabel("1  <<< ");
			greaterThan.setForeground(Color.WHITE);
			greaterThan.setHorizontalAlignment(SwingConstants.TRAILING);
			greaterThan.setFont(new Font("IMPACT", Font.PLAIN, 30));
			greaterThan.setBounds(90, 336, 180, 61);
			panel2.add(greaterThan);

			// Label for UpperLimit
			JLabel smallerThan = new JLabel();
			smallerThan.setForeground(Color.WHITE);
			smallerThan.setHorizontalAlignment(SwingConstants.LEADING);
			smallerThan.setFont(new Font("IMPACT", Font.PLAIN, 30));
			smallerThan.setBounds(566, 336, 180, 61);
			panel2.add(smallerThan);

			// Label for closing the window (used as a button)
			JLabel close = new JLabel("X");
			close.addMouseListener(new MouseAdapter() {
				@Override
				public void mouseClicked(MouseEvent e) {
					System.exit(0);
				}
			});
			close.setForeground(Color.WHITE);
			close.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 31));
			close.setBounds(newframe.getWidth() - 30, 2, 100, 42);
			panel2.add(close);

			// Title of the Window
			JLabel gtn = new JLabel(" GUESS THE NUMBER: ");
			gtn.setFont(new Font("Tahoma", Font.BOLD, 50));
			gtn.setBounds(0, 68, panel2.getWidth(), 100);
			gtn.setHorizontalAlignment(SwingConstants.CENTER);
			gtn.setForeground(Color.WHITE);
			panel2.add(gtn);

			// Label for telling the range from which the number was chosen at random
			// ,Depending on the Difficulty Chosen.
			JLabel ig = new JLabel();
			ig.setHorizontalAlignment(SwingConstants.CENTER);
			ig.setForeground(Color.WHITE);
			ig.setFont(new Font("Yu Gothic UI Light", Font.BOLD, 25));
			ig.setBounds(100, 150, 639, 100);
			if (Difficulty == "EASY") {
				number = rand.nextInt(100);
				smallerThan.setText(" <<< 100");
				ig.setText(
						"<html><div style='text-align: center;'>I Choose a number between 1-100<br>You got a total of 10 chances to get the Correct answer</div></html>");
			} else if (Difficulty == "MEDIUM") {
				number = rand.nextInt(5000);
				smallerThan.setText(" <<< 5000");
				ig.setText(
						"<html><div style='text-align: center;'>I Choose a number between 1-5000<br>You got a total of 10 chances to get the Correct answer</div></html>");
			} else if (Difficulty == "HARD") {
				number = rand.nextInt(10000);
				smallerThan.setText(" <<< 10000");
				ig.setText(
						"<html><div style='text-align: center;'>I Choose a number between 1-10000<br>You got a total of 10 chances to get the Correct answer</div></html>");
			}
			panel2.add(ig);

			// Entry Field for taking Answers
			JTextField textField = new JTextField();
			textField.setBorder(null);
			textField.setHorizontalAlignment(SwingConstants.CENTER);
			textField.setFont(new Font("Trebuchet MS", Font.BOLD, 50));
			textField.setBounds(311, 339, 216, 65);
			panel2.add(textField);
			textField.setColumns(10);

			// Submit label
			JLabel label = new JLabel();
			label.setBounds(390, 417, 60, 60);
			Image check = new ImageIcon(Syspath + File.separator + "Images\\check.png").getImage()
					.getScaledInstance(label.getWidth(), label.getHeight(), Image.SCALE_SMOOTH);
			label.setIcon(new ImageIcon(check));
			label.addMouseListener(new MouseAdapter() {
				@Override
				public void mouseClicked(MouseEvent e) {
					count++;
					if (count == 3) {
						progressBar.setForeground(Color.YELLOW);
					} else if (count == 6) {
						progressBar.setForeground(Color.ORANGE);
					} else if (count == 9) {
						progressBar.setForeground(Color.RED);
					}
					progressBar.setValue(count * 10);

					String path = "";
					if (count * 10 == 100) {
						path = "YOU LOST";
						stopAllSounds();
						playSound(Syspath + File.separator + "Sounds\\dun.wav");
						Result(path);
						newframe.dispose();
						count = 0;
					} else if (Integer.parseInt(textField.getText()) == number) {
						path = "YOU WON";
						stopAllSounds();
						playSound(Syspath + File.separator + "Sounds\\tada.wav");
						Result(path);
						newframe.dispose();
						count = 0;

					} else if (Integer.parseInt(textField.getText()) > number) {
						playSound(Syspath + File.separator + "Sounds/wrong.wav");
						path = "HIGH";
						Result_imi(path);
					} else if (Integer.parseInt(textField.getText()) < number) {
						playSound(Syspath + File.separator + "Sounds/wrong.wav");
						path = "LOW";
						Result_imi(path);
					}
				}
			});
			panel2.add(label);

			// Label for Background GIF
			JLabel main = new JLabel();
			main.setBounds(0, 0, panel2.getWidth(), panel2.getHeight());
			Image mainbg = new ImageIcon(Syspath + File.separator + "Images\\main.gif").getImage()
					.getScaledInstance(main.getWidth(), main.getHeight(), Image.SCALE_DEFAULT);
			main.setIcon(new ImageIcon(mainbg));
			panel2.add(main);

			// Z-Order
			panel2.setComponentZOrder(progressBar, 1);
			panel2.setComponentZOrder(greaterThan, 1);
			panel2.setComponentZOrder(smallerThan, 2);
			panel2.setComponentZOrder(close, 3);
			panel2.setComponentZOrder(gtn, 4);
			panel2.setComponentZOrder(ig, 5);
			panel2.setComponentZOrder(textField, 6);
			panel2.setComponentZOrder(label, 7);

			newframe.setVisible(true);
			newframe.setShape(new RoundRectangle2D.Double(0, 0, newframe.getWidth(), newframe.getHeight(), 20, 20));
		});
		mechanicsThread.start();

	}

	// Result Function
	public static void Result(String result) {
		JFrame frame_res = new JFrame();
		frame_res.setUndecorated(true);
		frame_res.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame_res.setSize(300, 100);
		frame_res.setLayout(null);
		frame_res.setLocationRelativeTo(null);

		JLabel label_res = new JLabel();
		label_res.setFont(new Font("Trebuchet MS", Font.BOLD, 50));
		label_res.setText(result);
		label_res.setSize(300, 80);
		label_res.setHorizontalAlignment(SwingConstants.CENTER);
		frame_res.add(label_res);

		JLabel chosennum = new JLabel();
		chosennum.setText("The number is:" + number);
		chosennum.setFont(new Font("Trebuchet MS", Font.BOLD, 11));
		chosennum.setBounds((frame_res.getWidth() - 115) / 2, frame_res.getHeight() - 25, 115, 10);
		frame_res.add(chosennum);

		frame_res.setVisible(true);
		frame_res.setShape(new RoundRectangle2D.Double(0, 0, frame_res.getWidth(), frame_res.getHeight(), 20, 20));
		Timer timer = new Timer(4000, new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				frame_res.dispose();
			}
		});
		timer.setRepeats(false);
		timer.start();
	}

	// Intermediate Result Function
	public static void Result_imi(String result) {
		JFrame frame_res = new JFrame();
		frame_res.setUndecorated(true);
		frame_res.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame_res.setSize(300, 100);
		frame_res.setLocationRelativeTo(null);

		JLabel label_res = new JLabel();
		label_res.setFont(new Font("Trebuchet MS", Font.BOLD, 50));
		label_res.setText(result);
		label_res.setSize(300, 100);
		label_res.setHorizontalAlignment(SwingConstants.CENTER);
		frame_res.add(label_res);
		frame_res.setVisible(true);
		frame_res.setShape(new RoundRectangle2D.Double(0, 0, frame_res.getWidth(), frame_res.getHeight(), 20, 20));
		Timer timer = new Timer(2000, new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				frame_res.dispose();
			}
		});
		timer.setRepeats(false);
		timer.start();
	}

	// MAIN LOBBY STARTS FROM HERE(Constructor of the Lobby Class)
	public Lobby() {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 450, 450);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(0, 0, 0, 0));

		setContentPane(contentPane);
		contentPane.setLayout(null);

		JPanel panel = new JPanel();
		panel.setBounds(0, 0, 470, 461);
		contentPane.add(panel);
		panel.setLayout(null);

		JPanel back = new BgPanel();
		back.setLayout(null);
		back.setBounds(0, 0, 470, 451);
		panel.add(back, 0);

		JLabel exit = new JLabel("X");
		exit.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				System.exit(0);
			}
		});
		exit.setForeground(SystemColor.textHighlightText);
		exit.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 31));
		exit.setBounds(415, 2, 83, 42);
		back.add(exit);

		String[] Difficulty = { "EASY", "MEDIUM", "HARD" };
		JComboBox<String> diff = new JComboBox<>(Difficulty);
		diff.setFont(new Font("Microsoft YaHei", Font.BOLD, 27));
		diff.setBounds(145, 345, 173, 41);
		diff.setBorder(null);
		panel.add(diff);

		JLabel play = new JLabel();
		play.setBounds(163, 131, 145, 142);
		play.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				String Difficulty = diff.getSelectedItem().toString();
				playSound(Syspath + File.separator + "Sounds\\29d52dde-5703-4d71-a42b-fb6f2a1463fc.877f0.wav");
				mechanics(Difficulty);

			}

		});
		play.setForeground(SystemColor.textHighlightText);
		play.setFont(new Font("Microsoft PhagsPa", Font.BOLD, 31));
		panel.add(play);

	}

}
