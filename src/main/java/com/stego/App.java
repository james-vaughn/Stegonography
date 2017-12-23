package com.stego;

import java.io.*;

public class App
{
    public static void main( String[] args ) {
        StringBuilder message = new StringBuilder();

        // get message to encode
        try (BufferedReader reader = new BufferedReader(new FileReader("message.txt"))){
            String line;

            while((line = reader.readLine()) != null) {
                message.append(line);
                message.append("\n");
            }
        } catch(IOException e) {
            System.err.println(e);
        }

        try {
            EncodeMessage("InputImages/moon.png",
                    "OutputImages/moon_out.png",
                    message.toString());
        } catch(IOException e) {
            System.err.println(e);
        }

        try {
            DecodeMessage("OutputImages/moon_out.png");
        } catch(IOException e) {
            System.err.println(e);
        }
    }

    public static void EncodeMessage(String inputFileName, String outputFileName, String message) throws IOException{
        StegoEncoder encoder = new StegoEncoder(inputFileName);

        encoder.Encode(message);
        encoder.WriteImage(outputFileName);

    }

    public static void DecodeMessage(String fileName) throws IOException {
        StegoEncoder decoder = new StegoEncoder(fileName);

        System.out.println(decoder.Decode());
    }
}
