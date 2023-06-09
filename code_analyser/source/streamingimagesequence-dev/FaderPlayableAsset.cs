﻿using UnityEngine;
using UnityEngine.Playables;
using UnityEngine.Timeline;

namespace Unity.StreamingImageSequence {

[System.Serializable] 
internal class FaderPlayableAsset : PlayableAsset, ITimelineClipAsset {
    public ClipCaps clipCaps {
        get {
            return ClipCaps.Extrapolation;
        }
    }

    public override Playable CreatePlayable(PlayableGraph graph, GameObject go) {
        var bh = new FaderPlayableBehaviour();
        return ScriptPlayable<FaderPlayableBehaviour>.Create(graph, bh);
    }

    internal void SetColor(Color color) { m_color = color; }
    internal Color GetColor() { return m_color;}
    internal void SetFadeType(FadeType fadeType) { m_fadeType = fadeType;}
    internal FadeType GetFadeType() { return m_fadeType;}

//----------------------------------------------------------------------------------------------------------------------
    [SerializeField] private Color m_color = Color.black;
    [SerializeField] private FadeType m_fadeType = FadeType.FADE_IN;

//----------------------------------------------------------------------------------------------------------------------

}


}