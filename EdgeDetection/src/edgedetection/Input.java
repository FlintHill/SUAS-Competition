/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package edgedetection;

import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

/**
 *
 * @author phusisian
 */
public class Input extends KeyAdapter
{
    private int dx, dy;
    public Input()
    {
        dx = 0; dy = 0;
    }
    public void keyPressed(KeyEvent e)
    {
        int keyCode = e.getKeyCode();
        if(keyCode == e.VK_LEFT)
        {
            dx = -5;
        }
        if(keyCode == e.VK_RIGHT)
        {
            dx = 5;
        }
        if(keyCode == e.VK_UP)
        {
            dy = -5;
        }
        if(keyCode == e.VK_DOWN)
        {
            dy = 5;
        }
    }
    public void keyReleased(KeyEvent e)
    {
        int keyCode = e.getKeyCode();
        if(keyCode == e.VK_LEFT)
        {
            dx = 0;
        }
        if(keyCode == e.VK_RIGHT)
        {
            dx = 0;
        }
        if(keyCode == e.VK_UP)
        {
            dy = 0;
        }
        if(keyCode == e.VK_DOWN)
        {
            dy = 0;
        }
    }
    
    public int getDx(){return dx;}
    public int getDy(){return dy;}
}
