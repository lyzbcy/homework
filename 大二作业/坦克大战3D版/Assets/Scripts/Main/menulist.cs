using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class menulist : MonoBehaviour
{
    public GameObject MenuList;
    public Button settingButton;

   


    
    

    [SerializeField] private bool menuKeys = true;
    [SerializeField] private AudioSource bgmSound;
    [SerializeField] private bool onclick = false;

    void Start()
    {
        //确保一开始是隐藏的
        MenuList.SetActive(false);

      

        // 绑定按钮点击事件
        settingButton.onClick.AddListener(OnSettingButtonClick);
    }

    void OnSettingButtonClick()
    {
        onclick = true;
    }

    void Update()
    {
        if (menuKeys)
        {
            if (Input.GetKeyDown(KeyCode.Escape) || onclick)
            {
               
                MenuList.SetActive(true);
                menuKeys = false;
                Time.timeScale = 0;
                bgmSound.Pause();
                onclick = false;
                
            }
        }
        else if (Input.GetKeyDown(KeyCode.Escape))
        {
            MenuList.SetActive(false);
            menuKeys = true;
            Time.timeScale = 1;
            bgmSound.Play();
        }
    }

    public void Return() // 返回游戏
    {
        MenuList.SetActive(false);
        menuKeys = true;
        Time.timeScale = 1;
        bgmSound.Play();
    }

    public void Restart() // 重新开始
    {
        SceneManager.LoadScene(1);
        Time.timeScale = 1;
        MenuList.SetActive(false);
        menuKeys = true;
        bgmSound.Play();
    }

    public void Exit() // 返回主菜单
    {
        SceneManager.LoadScene(0);
        Time.timeScale = 1;
    }

  

   

   

    

    public void Load_click()
    {
        
    }

   
}