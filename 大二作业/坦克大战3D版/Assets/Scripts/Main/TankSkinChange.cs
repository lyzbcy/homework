using UnityEngine;

public class TankSkinChange : MonoBehaviour
{
    // 挂载所有需要切换材质的部件
    public MeshRenderer[] tankRenderers;

    // 存储不同的材质
    public Material[] materials;

    // 当前材质索引
    private int currentMaterialIndex = 0;

    void Start()
    {
        // 从 PlayerPrefs 加载保存的材质索引
        currentMaterialIndex = PlayerPrefs.GetInt("TankMaterialIndex", 0);

        // 设置初始材质
        SetTankMaterial(currentMaterialIndex);
    }

    // 切换坦克皮肤的方法
    public void ChangeTankSkin()
    {
        // 更新材质索引
        currentMaterialIndex = (currentMaterialIndex + 1) % materials.Length;

        // 保存当前材质索引到 PlayerPrefs
        PlayerPrefs.SetInt("TankMaterialIndex", currentMaterialIndex);

        // 切换所有部件的材质
        SetTankMaterial(currentMaterialIndex);
    }

    // 获取当前材质索引
    public int GetCurrentMaterialIndex()
    {
        return currentMaterialIndex;
    }

    // 设置当前材质索引并更新材质
    public void SetCurrentMaterialIndex(int materialIndex)
    {
        if (materialIndex >= 0 && materialIndex < materials.Length)
        {
            currentMaterialIndex = materialIndex;
            SetTankMaterial(currentMaterialIndex);
        }
        else
        {
            Debug.LogWarning("材质索引无效: " + materialIndex);
        }
    }

    // 设置坦克材质
    private void SetTankMaterial(int materialIndex)
    {
        foreach (MeshRenderer renderer in tankRenderers)
        {
            renderer.material = materials[materialIndex];
        }
    }
}