using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Tank_Attack : MonoBehaviour
{
    public GameObject shellPrefab;
    public KeyCode fireKey = KeyCode.Space;
    public float shellSpeed = 10;
    public AudioClip shotAudio;

    private Transform firePoint;
    void Start()
    {
        firePoint = transform.Find("FirePoint");
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(fireKey)) {
            AudioSource.PlayClipAtPoint(shotAudio, transform.position);
            GameObject go = GameObject.Instantiate(shellPrefab, firePoint.position, firePoint.rotation) as GameObject;  //在发射点位置实例化子弹
            go.GetComponent<Rigidbody>().velocity = go.transform.forward * shellSpeed;

        }
    }
}
