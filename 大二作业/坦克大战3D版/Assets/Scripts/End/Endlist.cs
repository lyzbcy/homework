using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Endlist : MonoBehaviour
{
    
    


    // Update is called once per frame
    void Update()
    {

       
    }
    public void Restart()//重新开始
    {
        SceneManager.LoadScene(1);
        Time.timeScale = 1;
    }

    public void Exit()//返回主菜单
    {
        SceneManager.LoadScene(0);
        Time.timeScale = 1;
    }
}
