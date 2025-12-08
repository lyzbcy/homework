using UnityEngine;
using UnityEngine.UI;

public class Scene2Manager : MonoBehaviour
{
    public Text winnerText;

    void Start()
    {
        // 读取胜利坦克的信息
        string winnerTank = PlayerPrefs.GetString("WinnerTank", "Unknown");

        // 显示胜利坦克的信息
        winnerText.text = winnerTank + " 获胜!";
    }
}