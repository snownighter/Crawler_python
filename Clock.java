import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.Timer;
import java.util.TimerTask;

public class Clock extends JFrame {
    private JLabel timeLabel;
    private JLabel dateLabel;
    private JTextArea recordArea;
    private JButton recordButton;
    private JButton saveButton;
    private SimpleDateFormat timeFormat;
    private SimpleDateFormat dateFormat;
    private List<String> timeRecords;

    public Clock() {
        setTitle("Clock");
        setSize(300, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        timeLabel = new JLabel();
        dateLabel = new JLabel();
        recordArea = new JTextArea();
        recordButton = new JButton("Record Time");
        saveButton = new JButton("Save to File");
        timeRecords = new ArrayList<>();

        timeLabel.setFont(new Font("Arial", Font.BOLD, 24));
        dateLabel.setFont(new Font("Arial", Font.PLAIN, 18));
        recordArea.setFont(new Font("Arial", Font.PLAIN, 14));
        recordButton.setFont(new Font("Arial", Font.PLAIN, 14));
        saveButton.setFont(new Font("Arial", Font.PLAIN, 14));

        timeLabel.setHorizontalAlignment(SwingConstants.CENTER);
        dateLabel.setHorizontalAlignment(SwingConstants.CENTER);

        timeFormat = new SimpleDateFormat("HH:mm:ss");
        dateFormat = new SimpleDateFormat("EEEE, MMMM d, yyyy", Locale.ENGLISH);

        setLayout(new BorderLayout());

        JPanel topPanel = new JPanel(new GridLayout(2, 1));
        topPanel.add(timeLabel);
        topPanel.add(dateLabel);

        JPanel bottomPanel = new JPanel(new GridLayout(1, 2));
        bottomPanel.add(recordButton);
        bottomPanel.add(saveButton);

        add(topPanel, BorderLayout.NORTH);
        add(new JScrollPane(recordArea), BorderLayout.CENTER);
        add(bottomPanel, BorderLayout.SOUTH);

        setVisible(true);

        startClock();
        addRecordButtonListener();
        addSaveButtonListener();
    }

    private void startClock() {
        Timer timer = new Timer(true);
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                SwingUtilities.invokeLater(() -> {
                    String time = timeFormat.format(new Date());
                    String date = dateFormat.format(new Date());
                    timeLabel.setText(time);
                    dateLabel.setText(date);
                });
            }
        }, 0, 1000);
    }

    private void addRecordButtonListener() {
        recordButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String currentTime = timeFormat.format(new Date());
                timeRecords.add(currentTime);
                updateRecordArea();
            }
        });
    }

    private void addSaveButtonListener() {
        saveButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                saveRecordsToFile();
            }
        });
    }

    private void updateRecordArea() {
        StringBuilder sb = new StringBuilder();
        for (String record : timeRecords) {
            sb.append(record).append("\n");
        }
        recordArea.setText(sb.toString());
    }

    private void saveRecordsToFile() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("time_records.txt"))) {
            for (String record : timeRecords) {
                writer.write(record);
                writer.newLine();
            }
            JOptionPane.showMessageDialog(this, "Records saved to time_records.txt");
        } catch (IOException e) {
            JOptionPane.showMessageDialog(this, "Error saving records to file", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Clock());
    }
}
