using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class LoadGame : MonoBehaviour
{
    public GameObject tank1;
    public GameObject tank2;
    public Text loadSuccessText; // 引用提示文本

    void Start()
    {
        // 确保提示文本开始时是隐藏的
        loadSuccessText.gameObject.SetActive(false);
    }

    public void OnLoadButtonClick()
    {
        // 调用加载游戏状态的方法
        LoadGameState();
        Debug.Log("游戏已加载！");

        // 显示读档成功的提示
        ShowLoadSuccessMessage();
    }

    public void LoadGameState()
    {
        // 加载坦克1的信息
        LoadTankState("Tank1", tank1);

        // 加载坦克2的信息
        LoadTankState("Tank2", tank2);
    }

    void LoadTankState(string tankName, GameObject tank)
    {
        // 获取坦克的Transform和TankHealth组件
        Transform tankTransform = tank.transform;
        TankHealth tankHealth = tank.GetComponent<TankHealth>();
        TankSkinChange tankSkinChange = tank.GetComponent<TankSkinChange>();

        // 加载位置
        tankTransform.position = new Vector3(
            PlayerPrefs.GetFloat(tankName + "PosX"),
            PlayerPrefs.GetFloat(tankName + "PosY"),
            PlayerPrefs.GetFloat(tankName + "PosZ")
        );

        // 加载朝向
        tankTransform.rotation = Quaternion.Euler(
            PlayerPrefs.GetFloat(tankName + "RotX"),
            PlayerPrefs.GetFloat(tankName + "RotY"),
            PlayerPrefs.GetFloat(tankName + "RotZ")
        );

        // 加载血量
        tankHealth.hp = PlayerPrefs.GetInt(tankName + "Health");
        tankHealth.UpdateHealthDisplay(); // 更新血量显示

        // 加载材质索引
        tankSkinChange.SetCurrentMaterialIndex(PlayerPrefs.GetInt(tankName + "Material"));
    }

    public void ShowLoadSuccessMessage()
    {
        // 显示提示文本，并包含加载成功提示
        loadSuccessText.text = "游戏已加载";
        loadSuccessText.gameObject.SetActive(true);

        // 启动协程，在一秒后隐藏提示文本
        StartCoroutine(HideLoadSuccessMessage());
    }

    private IEnumerator HideLoadSuccessMessage()
    {
        // 等待一秒
        yield return new WaitForSeconds(1f);

        // 隐藏提示文本
        loadSuccessText.gameObject.SetActive(false);
    }
}