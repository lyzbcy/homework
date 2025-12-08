using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class TankHealth : MonoBehaviour
{
    public int hp = 100;
    public GameObject tankExplosion;
    public AudioClip tankExplosionAudio;

    public Slider hpSlider;

    private int hpTotal;

    // Start is called before the first frame update
    void Start()
    {
        hpTotal = hp;
        UpdateHealthDisplay(); // 确保游戏开始时更新血量显示
    }

    // Update is called once per frame
    void Update()
    {

    }

    void TankDamage()
    {
        if (hp <= 0)
            return;

        hp -= Random.Range(10, 20);
        UpdateHealthDisplay();

        if (hp <= 0)
        {
            AudioSource.PlayClipAtPoint(tankExplosionAudio, transform.position);
            GameObject.Instantiate(tankExplosion, transform.position + Vector3.up, transform.rotation);
            GameObject.Destroy(this.gameObject);

            // 存储胜利坦克的信息
            if (gameObject.name == "Tank1")
            {
                PlayerPrefs.SetString("WinnerTank", "Tank2");
            }
            else if (gameObject.name == "Tank2")
            {
                PlayerPrefs.SetString("WinnerTank", "Tank1");
            }

            // 切换到场景2
            SceneManager.LoadScene(2);
            return;
        }
    }

    public void UpdateHealthDisplay()
    {
        hpSlider.value = (float)hp / hpTotal;
    }
}