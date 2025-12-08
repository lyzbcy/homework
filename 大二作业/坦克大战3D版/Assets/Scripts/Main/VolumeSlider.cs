using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class VolumeSlider : MonoBehaviour
{
    public Slider volumeSlider; // 滑动条
    public AudioSource audioSource; // 用于播放提示音的音频源
    public AudioClip hintSound; // 提示音

    void Start()
    {
        // 确保音频源和提示音已设置
        if (audioSource == null)
        {
            Debug.LogError("AudioSource is not assigned.");
            return;
        }
        if (hintSound == null)
        {
            Debug.LogError("Hint sound is not assigned.");
            return;
        }

        // 添加滑动条值变化监听器
        volumeSlider.onValueChanged.AddListener(OnVolumeChanged);

        // 添加EventTrigger组件并配置PointerUp事件
        AddEventTrigger(volumeSlider.gameObject, EventTriggerType.PointerUp, OnSliderPointerUp);
    }

    // 滑动条值变化时调用此方法
    void OnVolumeChanged(float value)
    {
        // 设置音量大小
        audioSource.volume = value;
    }

    // 滑动条停止移动时调用此方法
    void OnSliderPointerUp(BaseEventData eventData)
    {
        // 播放提示音
        PlayHintSound();
    }

    // 播放提示音
    void PlayHintSound()
    {
        audioSource.PlayOneShot(hintSound);
    }

    // 添加EventTrigger
    void AddEventTrigger(GameObject obj, EventTriggerType type, System.Action<BaseEventData> action)
    {
        EventTrigger trigger = obj.GetComponent<EventTrigger>();
        if (trigger == null)
        {
            trigger = obj.AddComponent<EventTrigger>();
        }

        EventTrigger.Entry entry = new EventTrigger.Entry();
        entry.eventID = type;
        entry.callback.AddListener((eventData) => { action.Invoke(eventData); });
        trigger.triggers.Add(entry);
    }
}