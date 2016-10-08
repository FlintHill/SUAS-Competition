/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package edgedetection;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import javax.swing.JFrame;

/**
 *
 * @author phusisian
 */
public class EdgeDetection extends JFrame{

    private BufferedImage image;
    private double[][] dColor;
    public EdgeDetection()
    {
        try {
            image = ImageIO.read(new File("/Users/phusisian/Desktop/Senior year/SUAS/targets 300.jpg"));
            dColor = new double[image.getWidth()][image.getHeight()];
        } catch (Exception e) {
        }
    }
    public void paint(Graphics g)
    {
        Image scaled = image.getScaledInstance((int)(500*((double)image.getWidth()/(double)image.getHeight())), (int)(500), Image.SCALE_AREA_AVERAGING);
        g.drawImage(scaled, 0, 0, null);
        setDColor();
        Image contrast = contrastImage().getScaledInstance((int)(500*((double)image.getWidth()/(double)image.getHeight())), (int)(500), Image.SCALE_AREA_AVERAGING);
        g.drawImage(contrast, (int)(500*((double)image.getWidth()/(double)image.getHeight())), 0, null);
        repaint();
    }
    
    private void setDColor()
    {
        for(int i = 0; i < image.getWidth(); i++)
        {
            for(int j = 0; j < image.getHeight(); j++)
            {
                if(i > 0 && j > 0)
                {
                    int rgb = image.getRGB(i, j);
                    int oldrgb = image.getRGB(i-1, j);
                    int oldrgbY = image.getRGB(i, j-1);
                    Color c3 = new Color(oldrgbY, true);
                    Color c2 = new Color(rgb, true);
                    Color c1 = new Color(oldrgb,true);
                    double dRedComp = Math.pow(c2.getRed()-c1.getRed(), 2);
                    double dGreenComp = Math.pow(c2.getGreen()-c1.getGreen(), 2);
                    double dBlueComp = Math.pow(c2.getBlue()-c1.getBlue(), 2);
                    double dr2 = Math.pow(c2.getRed()-c3.getRed(), 2);
                    double dg2 = Math.pow(c2.getGreen()-c3.getGreen(),2);
                    double db2 = Math.pow(c2.getBlue()-c3.getBlue(),2);
                    dColor[i][j]=Math.sqrt(dRedComp+dGreenComp+dBlueComp)+Math.sqrt(dr2+dg2+db2)/2.0;
                }else{
                    dColor[i][j]=0;
                }
            }
        }
    }
    
    public double greatestDColor()
    {
        double largestNum = 0;
        for(int i = 0; i < image.getWidth(); i++)
        {
            for(int j = 0; j < image.getHeight(); j++)
            {
                if(dColor[i][j] > largestNum)
                {
                    largestNum = dColor[i][j];
                }
                //System.out.print(dColor[i][j] + ", ");
                
                
            }
            //System.out.println("");
        }
        return largestNum;
    }
    
    private BufferedImage contrastImage()
    {
        BufferedImage img = new BufferedImage(image.getWidth(), image.getHeight(), BufferedImage.TYPE_INT_ARGB);
        Graphics g = img.createGraphics();
         double largestNum = greatestDColor();
         double maxDColor = Math.sqrt(3*Math.pow(255,2));
        for(int i = 0; i < img.getWidth(); i++)
        {
            for(int j = 0; j < img.getHeight(); j++)
            {
                if(dColor[i][j] > largestNum)
                {
                    largestNum = dColor[i][j];
                }
                //System.out.print(dColor[i][j] + ", ");
                
                g.setColor(Color.BLUE);
                //g.setColor(new Color(255-(int)(255*dColor[i][j]/maxDColor),255-(int)(255*dColor[i][j]/maxDColor),255-(int)(255*dColor[i][j]/maxDColor)));
                g.setColor(new Color(255-(int)(255*dColor[i][j]/largestNum),255-(int)(255*dColor[i][j]/largestNum),255-(int)(255*dColor[i][j]/largestNum)));
                g.drawLine(i,j,i,j);
                
            }
            //System.out.println("");
        }
        System.out.println(largestNum);
        return img;
    }
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) 
    {
        EdgeDetection f = new EdgeDetection();
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        f.setVisible(true);
        f.setResizable(true);
        f.setSize(1440, 900);
        // TODO code application logic here
    }
    
}
