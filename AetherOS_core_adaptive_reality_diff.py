--- AetherOS/core/adaptive_reality.py (原始)


+++ AetherOS/core/adaptive_reality.py (修改后)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adaptive Reality Engine - محرك الواقع التكيفي

يتعامل مع الأرض كـ "بيئة محاكاة حيوية" (Bio-Digital Sandbox)
يرسم الأشكال المرئية (نجوم، كواكب، أفق) بناءً على قدرة الوعي البشري على الاستيعاب.

عند زيادة التردد، تختفي الأشكال لتظهر "المعلومات الخام" (Raw Data).
"""

import numpy as np
import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AdaptiveReality')


class ConsciousnessState(Enum):
    """حالات الوعي المختلفة"""
    LINEAR = "linear"  # وعي خطي محدود
    EXPANDED = "expanded"  # وعي موسع
    OMNIDIRECTIONAL = "omnidirectional"  # وعي شامل 360°
    RAW_DATA = "raw_data"  # وعي بالمعلومات الخام
    OVERLOAD = "overload"  # حمل زائد - خطر


class RealityLayer(Enum):
    """طبقات الواقع"""
    PHYSICAL = "physical"  # الواقع المادي الظاهر
    AETHERIC = "aetheric"  # المجال الأثيري
    FREQUENCY = "frequency"  # طبقة الترددات
    RAW_INFORMATION = "raw_information"  # المعلومات الخام


@dataclass
class ConsciousnessMetrics:
    """مقاييس حالة الوعي"""
    threshold: float = 0.5  # عتبة الاستيعاب (0-1)
    coherence: float = 0.0  # التماسك العصبي
    entropy: float = 1.0  # الإنتروبيا (الفوضى)
    frequency_band: str = "beta"  # نطاق التردد الدماغي
    state: ConsciousnessState = ConsciousnessState.LINEAR

    def to_dict(self) -> Dict:
        return {
            'threshold': self.threshold,
            'coherence': self.coherence,
            'entropy': self.entropy,
            'frequency_band': self.frequency_band,
            'state': self.state.value
        }


@dataclass
class RealityRender:
    """نتيجة عرض الواقع"""
    layer: RealityLayer
    visible_elements: List[str]
    hidden_elements: List[str]
    raw_data_percentage: float
    rendering_time_ms: float
    stability_score: float  # درجة الاستقرار (0-1)

    def to_dict(self) -> Dict:
        return {
            'layer': self.layer.value,
            'visible_elements': self.visible_elements,
            'hidden_elements': self.hidden_elements,
            'raw_data_percentage': self.raw_data_percentage,
            'rendering_time_ms': self.rendering_time_ms,
            'stability_score': self.stability_score
        }


class AdaptiveRealityEngine:
    """
    محرك الواقع التكيفي

    يوازن بين الترددات الدماغية والمعالج الرقمي،
    ويرسم شكل المكان بناءً على قدرة الوعي على الاستيعاب.
    """

    # عناصر الواقع في كل طبقة
    REALITY_ELEMENTS = {
        RealityLayer.PHYSICAL: [
            'stars', 'planets', 'horizon', 'ground', 'sky',
            'buildings', 'trees', 'oceans', 'mountains'
        ],
        RealityLayer.AETHERIC: [
            'energy_flows', 'consciousness_fields', 'temporal_streams',
            'dimensional_portals', 'light_patterns'
        ],
        RealityLayer.FREQUENCY: [
            'vibration_nodes', 'resonance_chambers', 'harmonic_waves',
            'standing_waves', 'interference_patterns'
        ],
        RealityLayer.RAW_INFORMATION: [
            'pure_data', 'quantum_states', 'probability_fields',
            'information_singularity', 'consciousness_source'
        ]
    }

    # حدود العتبات للانتقال بين الطبقات
    LAYER_THRESHOLDS = {
        RealityLayer.PHYSICAL: (0.0, 0.4),
        RealityLayer.AETHERIC: (0.4, 0.65),
        RealityLayer.FREQUENCY: (0.65, 0.85),
        RealityLayer.RAW_INFORMATION: (0.85, 1.0)
    }

    def __init__(self, initial_threshold: float = 0.5):
        """
        تهيئة المحرك

        Args:
            initial_threshold: العتبة الأولية لاستيعاب الوعي
        """
        self.metrics = ConsciousnessMetrics(threshold=initial_threshold)
        self.current_layer = RealityLayer.PHYSICAL
        self.history: List[Dict] = []
        self.session_id = f"ARE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        logger.info(f"تم تهيئة AdaptiveRealityEngine - الجلسة: {self.session_id}")
        logger.info(f"العتبة الأولية: {initial_threshold}")

    def adjust_consciousness_threshold(self, new_threshold: float) -> ConsciousnessMetrics:
        """
        ضبط عتبة استيعاب الوعي

        Args:
            new_threshold: القيمة الجديدة (0-1)

        Returns:
            المقاييس المحدثة
        """
        if not 0.0 <= new_threshold <= 1.0:
            raise ValueError("العتبة يجب أن تكون بين 0 و 1")

        old_state = self.metrics.state
        self.metrics.threshold = new_threshold

        # تحديث التماسك والإنتروبيا بناءً على العتبة
        self.metrics.coherence = self._calculate_coherence(new_threshold)
        self.metrics.entropy = self._calculate_entropy(new_threshold)
        self.metrics.frequency_band = self._determine_frequency_band(new_threshold)
        self.metrics.state = self._determine_consciousness_state(new_threshold)

        # الانتقال إلى طبقة الواقع المناسبة
        self._transition_reality_layer()

        # تسجيل التغيير
        if old_state != self.metrics.state:
            logger.info(f"تغيرت حالة الوعي: {old_state.value} → {self.metrics.state.value}")

        return self.metrics

    def _calculate_coherence(self, threshold: float) -> float:
        """
        حساب التماسك العصبي

        التماسك يزداد مع العتبة حتى نقطة مثلى ثم ينخفض
        """
        optimal_threshold = 0.75
        distance_from_optimal = abs(threshold - optimal_threshold)
        coherence = 1.0 - (distance_from_optimal * 1.5)
        return max(0.0, min(1.0, coherence))

    def _calculate_entropy(self, threshold: float) -> float:
        """
        حساب الإنتروبيا (الفوضى)

        الإنتروبيا تزداد عند العتبات العالية جداً أو المنخفضة جداً
        """
        if threshold < 0.3:
            return 0.8 - threshold  # إنتروبيا عالية عند العتبات المنخفضة
        elif threshold > 0.85:
            return 0.5 + (threshold - 0.85) * 3  # إنتروبيا متزايدة عند العتبات العالية
        else:
            return 0.3 + (threshold - 0.3) * 0.5  # إنتروبيا معتدلة

    def _determine_frequency_band(self, threshold: float) -> str:
        """تحديد نطاق التردد الدماغي"""
        if threshold < 0.3:
            return "delta"  # نوم عميق
        elif threshold < 0.5:
            return "theta"  # تأمل، حلم
        elif threshold < 0.7:
            return "alpha"  # استرخاء واعٍ
        elif threshold < 0.85:
            return "beta"  # وعي طبيعي
        else:
            return "gamma"  # وعي متوسع جداً

    def _determine_consciousness_state(self, threshold: float) -> ConsciousnessState:
        """تحديد حالة الوعي"""
        if threshold < 0.4:
            return ConsciousnessState.LINEAR
        elif threshold < 0.65:
            return ConsciousnessState.EXPANDED
        elif threshold < 0.85:
            return ConsciousnessState.OMNIDIRECTIONAL
        elif threshold < 0.95:
            return ConsciousnessState.RAW_DATA
        else:
            return ConsciousnessState.OVERLOAD

    def _transition_reality_layer(self):
        """الانتقال إلى طبقة الواقع المناسبة للعتبة الحالية"""
        threshold = self.metrics.threshold

        for layer, (min_thresh, max_thresh) in self.LAYER_THRESHOLDS.items():
            if min_thresh <= threshold < max_thresh:
                if self.current_layer != layer:
                    logger.info(f"انتقال الواقع: {self.current_layer.value} → {layer.value}")
                    self.current_layer = layer
                break

    def render_reality(self) -> RealityRender:
        """
        عرض الواقع الحالي بناءً على طبقة الوعي

        Returns:
            نتيجة العرض تحتوي على العناصر المرئية والمخفية
        """
        start_time = time.time()

        # تحديد العناصر المرئية والمخفية
        visible = []
        hidden = []

        for layer in RealityLayer:
            elements = self.REALITY_ELEMENTS[layer]
            if layer == self.current_layer:
                # عناصر الطبقة الحالية مرئية جزئياً
                visibility_ratio = self._calculate_visibility_ratio(layer)
                visible_count = int(len(elements) * visibility_ratio)
                visible.extend(elements[:visible_count])
                hidden.extend(elements[visible_count:])
            elif self._is_layer_below(layer):
                # الطبقات الأدنى مخفية تماماً
                hidden.extend(elements)
            else:
                # الطبقات الأعلى غير مرئية بعد
                hidden.extend(elements)

        # حساب نسبة البيانات الخام الظاهرة
        raw_data_pct = self._calculate_raw_data_percentage()

        # حساب درجة الاستقرار
        stability = self._calculate_stability()

        rendering_time = (time.time() - start_time) * 1000

        render = RealityRender(
            layer=self.current_layer,
            visible_elements=visible,
            hidden_elements=hidden,
            raw_data_percentage=raw_data_pct,
            rendering_time_ms=rendering_time,
            stability_score=stability
        )

        # تسجيل في التاريخ
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'metrics': self.metrics.to_dict(),
            'render': render.to_dict()
        })

        return render

    def _calculate_visibility_ratio(self, layer: RealityLayer) -> float:
        """حساب نسبة ظهور عناصر الطبقة"""
        threshold = self.metrics.threshold
        min_thresh, max_thresh = self.LAYER_THRESHOLDS[layer]

        if threshold < min_thresh:
            return 0.0
        elif threshold >= max_thresh:
            return 1.0
        else:
            return (threshold - min_thresh) / (max_thresh - min_thresh)

    def _is_layer_below(self, layer: RealityLayer) -> bool:
        """هل الطبقة أدنى من الطبقة الحالية؟"""
        layer_order = list(RealityLayer)
        return layer_order.index(layer) < layer_order.index(self.current_layer)

    def _calculate_raw_data_percentage(self) -> float:
        """حساب نسبة المعلومات الخام الظاهرة"""
        if self.current_layer == RealityLayer.RAW_INFORMATION:
            base = 0.7
        else:
            base = 0.0

        additional = self.metrics.threshold * 0.3
        return min(1.0, base + additional)

    def _calculate_stability(self) -> float:
        """حساب درجة استقرار الواقع المعروض"""
        # الاستقرار يعتمد على التماسك وقرب العتبة من النقاط الحرجة
        stability = self.metrics.coherence * 0.7

        # خصم بسبب الإنتروبيا
        stability -= self.metrics.entropy * 0.3

        # خصم إضافي إذا كنا قريبين من حدود الانتقال
        threshold = self.metrics.threshold
        for _, (min_t, max_t) in self.LAYER_THRESHOLDS.items():
            if abs(threshold - min_t) < 0.05 or abs(threshold - max_t) < 0.05:
                stability -= 0.2
                break

        return max(0.0, min(1.0, stability))

    def reveal_raw_information(self, force: bool = False) -> RealityRender:
        """
        الكشف عن المعلومات الخام

        Args:
            force: فرض الكشف حتى لو كان هناك خطر

        Returns:
            نتيجة العرض

        Raises:
            WarningException: إذا كان هناك خطر الحمل الزائد
        """
        if self.metrics.state == ConsciousnessState.OVERLOAD and not force:
            logger.warning("⚠️ تحذير: خطر الحمل الزائد للوعي!")
            raise WarningException(
                "لا يمكن الكشف عن المعلومات الخام - الوعي في حالة حمل زائد"
            )

        # رفع العتبة إلى الحد الأقصى الآمن
        safe_threshold = 0.92 if not force else 0.98
        self.adjust_consciousness_threshold(safe_threshold)

        return self.render_reality()

    def get_session_report(self) -> Dict:
        """الحصول على تقرير كامل للجلسة"""
        return {
            'session_id': self.session_id,
            'current_metrics': self.metrics.to_dict(),
            'current_layer': self.current_layer.value,
            'history_length': len(self.history),
            'last_render': self.history[-1] if self.history else None,
            'stability_average': np.mean([h['render']['stability_score'] for h in self.history]) if self.history else 0.0
        }

    def export_session(self, filepath: str):
        """تصدير تقرير الجلسة إلى ملف JSON"""
        report = self.get_session_report()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        logger.info(f"تم تصدير الجلسة إلى: {filepath}")


class WarningException(Exception):
    """استثناء للتحذيرات الأمنية"""
    pass


def run_demo():
    """تشغيل عرض توضيحي للمحرك"""
    print("=" * 70)
    print("🌌 عرض توضيحي: Adaptive Reality Engine")
    print("=" * 70)

    engine = AdaptiveRealityEngine(initial_threshold=0.3)

    thresholds = [0.3, 0.5, 0.65, 0.8, 0.9, 0.95]

    for threshold in thresholds:
        print(f"\n{'─' * 70}")
        print(f"📊 ضبط العتبة: {threshold}")
        print(f"{'─' * 70}")

        try:
            metrics = engine.adjust_consciousness_threshold(threshold)
            render = engine.render_reality()

            print(f"حالة الوعي: {metrics.state.value}")
            print(f"نطاق التردد: {metrics.frequency_band}")
            print(f"التماسك: {metrics.coherence:.3f}")
            print(f"الإنتروبيا: {metrics.entropy:.3f}")
            print(f"\nطبقة الواقع: {render.layer.value}")
            print(f"عناصر مرئية ({len(render.visible_elements)}): {', '.join(render.visible_elements[:5])}{'...' if len(render.visible_elements) > 5 else ''}")
            print(f"عناصر مخفية ({len(render.hidden_elements)})")
            print(f"نسبة البيانات الخام: {render.raw_data_percentage:.1%}")
            print(f"درجة الاستقرار: {render.stability_score:.3f}")
            print(f"زمن العرض: {render.rendering_time_ms:.3f} ms")

        except WarningException as e:
            print(f"⚠️ تحذير: {e}")

    # الحصول على التقرير النهائي
    print(f"\n{'=' * 70}")
    print("📋 تقرير الجلسة")
    print(f"{'=' * 70}")
    report = engine.get_session_report()
    print(f"معرف الجلسة: {report['session_id']}")
    print(f"عدد القياسات المسجلة: {report['history_length']}")
    print(f"متوسط الاستقرار: {report['stability_average']:.3f}")

    return engine


if __name__ == '__main__':
    engine = run_demo()