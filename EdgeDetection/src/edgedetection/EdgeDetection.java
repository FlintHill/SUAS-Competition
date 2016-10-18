/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package edgedetection;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.Point;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.ArrayList;
import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.Timer;

/**
 *
 * @author phusisian
 */
public class EdgeDetection extends JFrame implements ActionListener{

    private Color[] colorList = {Color.YELLOW, Color.RED, Color.BLUE, Color.GREEN, Color.MAGENTA, Color.ORANGE};
    private BufferedImage image;
    private double[][] dColor;
    private Input input = new Input();
    private Timer tickTimer = new Timer(10, this);
    private ArrayList<ArrayList<Point>> edgePoints = new ArrayList<ArrayList<Point>>();
    private double x, y;
    private BufferedImage contrast;
    public EdgeDetection()
    {
        addKeyListener(input);
        try {
            image = ImageIO.read(new File("/Users/phusisian/Desktop/Senior year/SUAS/targets 300 downScaled.jpg"));
            dColor = new double[image.getWidth()][image.getHeight()];
        } catch (Exception e) {
        }
        x=0;
        y=0;
        setDColor();
        contrast = contrastImage("COLOR_CODE", 30);
        
        tickTimer.setRepeats(true);
        tickTimer.setActionCommand("tick");
        tickTimer.start();
    }
    public void paint(Graphics g)
    {
        super.paint(g);
        //Image scaled = image.getScaledInstance((int)(500*((double)image.getWidth()/(double)image.getHeight())), (int)(500), Image.SCALE_AREA_AVERAGING);
        //g.drawImage(scaled, (int)x, (int)y, null);
        //g.drawImage(image, (int)x, (int)y, null);
        
        //Image contrast = contrastImage().getScaledInstance((int)(500*((double)image.getWidth()/(double)image.getHeight())), (int)(500), Image.SCALE_AREA_AVERAGING);
        //g.drawImage(contrast, (int)(x+(500*((double)image.getWidth()/(double)image.getHeight()))), (int)y, null);
        //g.drawImage(contrastImage(), (int)(x+image.getWidth()), (int)(y+image.getHeight()), null);
        g.drawImage(contrast, (int)(x), (int)(y), null);
        System.out.println("tick");
        g.drawString("X: " + Double.toString(x), 50, 50);
        g.drawString("Y: " + Double.toString(y), 50, 100);
        //repaint();
    }
    
    private void shadeShape(Graphics g, int x, int y, int width, int height, int threshold)//713x, 452y, width 54, height 54
    {
        g.setColor(Color.BLUE);
        g.drawRect(x, y, width, height);
        g.setColor(Color.RED);
        Point[][] pointArray = new Point[width][height];
        int pointListCount = 0;
        for(int j = y; j < y+height; j++)
        {
            boolean edgeFound = false;
            boolean insideFound = false;
            int pointCount = 0;
            Point[] points = new Point[2];
            for (int i = x; i < x + width; i++) 
            {
                if(pointCount < 2)
                {
                    if(!edgeFound)
                    {
                        if(dColor[i][j] > threshold)
                        {
                            points[pointCount]=new Point(i, j);
                            edgeFound = true;
                            pointCount++;
                        }
                    }else{
                        if(!insideFound)
                        {
                            if(dColor[i][j] < threshold)
                            {
                                insideFound = true;
                                edgeFound = false;
                            }
                        }
                    }
                }
            }
            try {
                g.drawLine((int)points[0].getX(), (int)points[0].getY(), (int)points[1].getX(), (int)points[1].getY());
                if(pointCount >= 2)
                {
                    pointArray[pointListCount] = points;
                    pointListCount++;
                }
            } catch (Exception e) {
            }
        }
        shadeOuterInnerBoxX(g, pointArray);
        shadeOuterInnerBoxY(g, pointArray);
        /*pointListCount = 0;
        Point[][] points = new Point[width][height];
        for (int i = x; i < x+width; i++)
        {
            boolean edgeFound = false;
            boolean insideFound = false;
            Point[] linePoints = new Point[2];
            int pointCount =0;
            for (int j = y; j < y+height; j++)
            {
                if(pointCount < 2)
                {
                    if(!edgeFound)
                    {
                        if(dColor[i][j]>threshold)
                        {
                            linePoints[pointCount]=new Point(i, j);
                            edgeFound = true;
                             pointCount++;
                        }
                    }else{
                        if(!insideFound)
                        {
                            if(dColor[i][j] < threshold)
                            {
                                insideFound = true;
                                edgeFound = false;
                            }
                        }
                    }
                } 
            }
            if(pointCount >= 2)
            {
                points[pointListCount] = linePoints;
                pointListCount++;
            }
        }
        shadeOuterInnerBoxY(g, points);*/
    }
    
    private int[] getXBounds(Point[][] points)
    {
        int smallestX = (int)points[0][0].getX();
        int biggestX = (int)points[0][1].getX();
        int lastNum = 0;
        for(int i = 0; i < points.length; i++)
        {
            try {
                if(points[i][0].getX() < smallestX)
                {
                    smallestX = (int)points[i][0].getX();
                }
                if(points[i][1].getX() > biggestX)
                {
                    biggestX = (int)points[i][1].getX();
                }
                lastNum++;
            } catch (Exception e) {
            }
        }
        int[] giveReturn = {smallestX, biggestX};
        return giveReturn;
    }
    
    private void shadeOuterInnerBoxX(Graphics g, Point[][] points)
    {
        int smallestX = (int)points[0][0].getX();
        int biggestX = (int)points[0][1].getX();
        int lastNum = 0;
        for(int i = 0; i < points.length; i++)
        {
            try {
                if(points[i][0].getX() < smallestX)
                {
                    smallestX = (int)points[i][0].getX();
                }
                if(points[i][1].getX() > biggestX)
                {
                    biggestX = (int)points[i][1].getX();
                }
                lastNum++;
            } catch (Exception e) {
            }
        }
        g.drawLine(smallestX, (int)points[0][0].getY(), smallestX, (int)points[lastNum-1][0].getY());
        g.drawLine(biggestX, (int)points[0][1].getY(), biggestX, (int)points[lastNum-1][1].getY());
    }
    
    private void shadeOuterInnerBoxY(Graphics g, Point[][] points)
    {
        /*
        int smallestY = (int)points[0][0].getY();
        int biggestY = (int)points[0][1].getY();
        int lastNum = 0;
        for(int i = 0; i < points.length; i++)
        {
            try {
                if(points[i][0].getY() < smallestY)
                {
                    smallestY = (int)points[i][0].getY();
                }
                if(points[i][1].getY() > biggestY)
                {
                    biggestY = (int)points[i][1].getY();
                }
                lastNum++;
            } catch (Exception e) {
            }
        }
        g.drawLine((int)points[0][0].getX(), smallestY, (int)points[lastNum-1][0].getX(), smallestY);
        g.drawLine((int)points[0][1].getX(), biggestY, (int)points[lastNum-1][1].getX(), biggestY);*/
        int[] xBounds = getXBounds(points);
        int highestY = (int)points[0][0].getY();
        boolean topFound = false;
        boolean bottomFound = false;
        for(int i = 0; i < points.length; i++)
        {
            if(points[i][0]!=null)
            {
                if(!topFound)
                {
                    g.drawLine(xBounds[0],(int)points[i][0].getY(), xBounds[1], (int)points[i][1].getY());
                    topFound = true;
                }
            }
        }
        for(int i = points.length-1; i > 0; i--) 
        {
            if(points[i][0]!=null)
            {
                if(!bottomFound)
                {
                    g.drawLine(xBounds[0],(int)points[i][0].getY(), xBounds[1], (int)points[i][1].getY());
                    bottomFound = true;
                }
            }
        }
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
    
    private BufferedImage contrastImage(String renderType, int threshold)
    {
        BufferedImage img = new BufferedImage(image.getWidth(), image.getHeight(), BufferedImage.TYPE_INT_ARGB);
        Graphics g = img.createGraphics();
         double largestNum = greatestDColor();
         double maxDColor = Math.sqrt(3*Math.pow(255,2));
        if(renderType.equals("SOFT_EDGES"))
        {
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
                    g.setColor(new Color((int)(255*dColor[i][j]/largestNum),(int)(255*dColor[i][j]/largestNum),(int)(255*dColor[i][j]/largestNum)));
                    g.drawLine(i,j,i,j);

                }
                //System.out.println("");
            }
        }else if(renderType.equals("STRESS_THRESHOLD"))
        {
            g.setColor(Color.BLACK);
            g.fillRect(0,0,img.getWidth(),img.getHeight());
            g.setColor(Color.WHITE);
            for(int i = 0; i < img.getWidth(); i++)
            {
                for(int j = 0; j < img.getHeight(); j++)
                {
                    if(dColor[i][j] > largestNum)
                    {
                        largestNum = dColor[i][j];
                    }
                    //System.out.print(dColor[i][j] + ", ");

                    
                    //g.setColor(new Color(255-(int)(255*dColor[i][j]/maxDColor),255-(int)(255*dColor[i][j]/maxDColor),255-(int)(255*dColor[i][j]/maxDColor)));
                    if(dColor[i][j] > threshold)
                    {
                        
                        g.drawLine(i,j,i,j);
                    }
                    //g.setColor(new Color((int)(255*dColor[i][j]/largestNum),(int)(255*dColor[i][j]/largestNum),(int)(255*dColor[i][j]/largestNum)));
                    

                }
                //System.out.println("");
            }
        }else if(renderType.equals("COLOR_CODE"))
        {
            double colorDivide = (double)largestNum/((double)colorList.length-1);
            int upperThreshold = 30;
            for(int i = 0; i < img.getWidth(); i++)
            {
                for(int j = 0; j < img.getHeight(); j++)
                {
                    //if(dColor[i][])
                    g.setColor(colorList[(int)(dColor[i][j]/colorDivide)]);
                    g.drawLine(i, j, i, j);
                }
            }
        }
        //shadeShape(g,723,472,38,35,40);
        shadeShape(g,710,460,57,57,40);
        //shadeShape(g, 513,369,88,103,40);
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

    @Override
    public void actionPerformed(ActionEvent e) 
    {
        x+= input.getDx();
        y+= input.getDy();
        if(input.getDx() != 0 || input.getDy() != 0)
        {
            repaint();
        }
        //System.out.println("Hi");
    }
    
}
