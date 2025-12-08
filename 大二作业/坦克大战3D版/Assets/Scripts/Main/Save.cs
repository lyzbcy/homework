using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class SaveGame : MonoBehaviour
{
    public GameObject tank1;
    public GameObject tank2;
    public Text saveSuccessText; // 引用提示文本

    public string savePath;

    void Start()
    {
        // 确保提示文本开始时是隐藏的
        saveSuccessText.gameObject.SetActive(false);

        // 设置保存路径
        savePath = Application.persistentDataPath + "/SaveData";

        // 获取 RectTransform 组件
        RectTransform rectTransform = saveSuccessText.GetComponent<RectTransform>();
    }

    public void OnSaveButtonClick()
    {
        // 调用保存游戏状态的方法
        SaveGameState();
        Debug.Log("游戏已保存！路径：" + savePath);

        // 显示存档成功的提示
        ShowSaveSuccessMessage();
    }

    public void SaveGameState()
    {
        // 保存坦克1的信息
        SaveTankState("Tank1", tank1);

        // 保存坦克2的信息
        SaveTankState("Tank2", tank2);

        // 确保保存到磁盘
        PlayerPrefs.Save();
    }

    void SaveTankState(string tankName, GameObject tank)
    {
        // 获取坦克的Transform和TankHealth组件
        Transform tankTransform = tank.transform;
        TankHealth tankHealth = tank.GetComponent<TankHealth>();
        TankSkinChange tankSkinChange = tank.GetComponent<TankSkinChange>();

        // 保存位置
        PlayerPrefs.SetFloat(tankName + "PosX", tankTransform.position.x);
        PlayerPrefs.SetFloat(tankName + "PosY", tankTransform.position.y);
        PlayerPrefs.SetFloat(tankName + "PosZ", tankTransform.position.z);

        // 保存朝向
        PlayerPrefs.SetFloat(tankName + "RotX", tankTransform.rotation.eulerAngles.x);
        PlayerPrefs.SetFloat(tankName + "RotY", tankTransform.rotation.eulerAngles.y);
        PlayerPrefs.SetFloat(tankName + "RotZ", tankTransform.rotation.eulerAngles.z);

        // 保存血量
        PlayerPrefs.SetInt(tankName + "Health", tankHealth.hp);

        // 保存材质索引
        PlayerPrefs.SetInt(tankName + "Material", tankSkinChange.GetCurrentMaterialIndex());
    }

    public void ShowSaveSuccessMessage()
    {
        // 显示提示文本，并包含保存路径
        saveSuccessText.text = "游戏已保存至" + savePath;
        saveSuccessText.gameObject.SetActive(true);

        // 启动协程，在一秒后隐藏提示文本
        StartCoroutine(HideSaveSuccessMessage());
    }

    private IEnumerator HideSaveSuccessMessage()
    {
        // 等待一秒
        yield return new WaitForSeconds(1f);

        // 隐藏提示文本
        saveSuccessText.gameObject.SetActive(false);
    }
}