using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;

public class StartGame : MonoBehaviour
{
    [SerializeField] private bool menuKeys = true;

    public void StartMenu()
    {
        if (menuKeys == true)
            SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1);
    }

    public void ExitGame()
    {
        if (menuKeys == true)
            Application.Quit();
    }

    public GameObject GreenList;

    void Start()
    {
        //确保一开始是隐藏的
        GreenList.SetActive(false);

    }

    public void GreenHand_Click()
    {
        if (menuKeys)
        {
            GreenList.SetActive(true);
            menuKeys = false;
        }
    }

    public void return_from_GreenList()
    {
        if (menuKeys==false)
        {
            GreenList.SetActive(false);
            menuKeys = true;
        }
    }


}