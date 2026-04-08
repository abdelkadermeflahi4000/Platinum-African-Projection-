--- beyond_the_facade/src/reality_engine.py (原始)


+++ beyond_the_facade/src/reality_engine.py (修改后)
"""
Beyond the Facade - Core Reality Engine
محرك الواقع الأساسي - مشروع ما وراء الواجهة

This module implements the foundational reality simulation engine
that models restricted coordinate systems and perspective expansion.
"""

from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import time
import math


class PerspectiveType(Enum):
    """أنواع المنظور الإدراكي"""
    LINEAR = "linear"  # منظور خطي محدود
    OMNIDIRECTIONAL = "omnidirectional"  # منظور شامل 360°
    MULTIDIMENSIONAL = "multidimensional"  # منظور متعدد الأبعاد


class RealityState(Enum):
    """حالات الواقع"""
    CLOSED = "closed"  # مغلق - حدود ضيقة
    EXPANDING = "expanding"  # في التوسع
    OPEN = "open"  # مفتوح - كشف الطبقات المخفية
    TEMPORAL_LOOP = "temporal_loop"  # حلقة زمنية مكررة


@dataclass
class BoundingBox:
    """نظام الإحداثيات المقيد للواقع الحالي"""
    min_x: float = -100.0
    max_x: float = 100.0
    min_y: float = -100.0
    max_y: float = 100.0
    min_z: float = -100.0
    max_z: float = 100.0

    def is_within_bounds(self, x: float, y: float, z: float) -> bool:
        """التحقق مما إذا كانت النقطة ضمن الحدود"""
        return (self.min_x <= x <= self.max_x and
                self.min_y <= y <= self.max_y and
                self.min_z <= z <= self.max_z)

    def expand(self, factor: float = 2.0) -> 'BoundingBox':
        """توسيع الحدود بعامل معين"""
        return BoundingBox(
            min_x=self.min_x * factor,
            max_x=self.max_x * factor,
            min_y=self.min_y * factor,
            max_y=self.max_y * factor,
            min_z=self.min_z * factor,
            max_z=self.max_z * factor
        )


@dataclass
class HiddenLayer:
    """طبقة واقع مخفية"""
    id: str
    name: str
    description: str
    unlock_condition: str  # شرط الكشف
    is_revealed: bool = False
    coordinates: Optional[Dict[str, float]] = None


@dataclass
class TemporalLoop:
    """نمط الزمن الحلقي المكرر"""
    start_time: float = field(default_factory=time.time)
    loop_duration: float = 60.0  # مدة الحلقة بالثواني
    iteration_count: int = 0
    is_active: bool = True

    def get_current_position(self) -> float:
        """الحصول على الموقع الحالي في الحلقة الزمنية"""
        elapsed = time.time() - self.start_time
        return elapsed % self.loop_duration

    def break_loop(self) -> bool:
        """كسر الحلقة الزمنية"""
        if self.iteration_count >= 3:  # شرط كسر الحلقة
            self.is_active = False
            return True
        return False


class RealityEngine:
    """
    محرك الواقع الأساسي
    Reality Engine for simulating bounded and expandable realities
    """

    def __init__(self, perspective: str = "linear", bounds: str = "atmosphere"):
        self.perspective = PerspectiveType(perspective)
        self.state = RealityState.CLOSED
        self.bounding_box = BoundingBox()
        self.hidden_layers: List[HiddenLayer] = []
        self.temporal_loop = TemporalLoop()
        self.awareness_level: float = 0.0  # مستوى الوعي من 0 إلى 1

        # Initialize default hidden layers
        self._initialize_hidden_layers()

    def _initialize_hidden_layers(self):
        """تهيئة طبقات الواقع المخفية الافتراضية"""
        self.hidden_layers = [
            HiddenLayer(
                id="layer_1",
                name="الطبقة الأثيرية",
                description="طبقة الطاقة الخفية خلف المادة الظاهرة",
                unlock_condition="perspective_shift_90"
            ),
            HiddenLayer(
                id="layer_2",
                name="الطبقة الزمنية الموازية",
                description="مسار زمني بديل يتقاطع مع الواقع الحالي",
                unlock_condition="temporal_loop_break"
            ),
            HiddenLayer(
                id="layer_3",
                name="الأرض الأخرى",
                description="واقع موازي كامل الأبعاد",
                unlock_condition="omnidirectional_awareness"
            )
        ]

    def describe(self) -> str:
        """وصف الحالة الحالية للواقع"""
        return f"""
=== حالة الواقع الحالي ===
المنظور: {self.perspective.value}
الحالة: {self.state.value}
مستوى الوعي: {self.awareness_level:.2%}
حدود النظام: ({self.bounding_box.min_x:.0f}, {self.bounding_box.max_x:.0f}) ×
              ({self.bounding_box.min_y:.0f}, {self.bounding_box.max_y:.0f}) ×
              ({self.bounding_box.min_z:.0f}, {self.bounding_box.max_z:.0f})
الطبقات المخفية المكتشفة: {sum(1 for l in self.hidden_layers if l.is_revealed)}/{len(self.hidden_layers)}
الحلقة الزمنية: {'نشطة' if self.temporal_loop.is_active else 'مكسورة'} (التكرار #{self.temporal_loop.iteration_count})
========================
        """.strip()

    def expand_awareness(self, mode: str = "gradual") -> bool:
        """
        توسيع الوعي وكسر الإغلاق الفكري

        Args:
            mode: نمط التوسع (gradual, sudden, omnidirectional)

        Returns:
            bool: نجاح عملية التوسع
        """
        if mode == "omnidirectional":
            target_awareness = 1.0
            self.perspective = PerspectiveType.OMNIDIRECTIONAL
        elif mode == "sudden":
            target_awareness = 0.8
        else:  # gradual
            target_awareness = min(self.awareness_level + 0.15, 1.0)

        # محاكاة عملية التوسع
        old_state = self.state
        self.awareness_level = target_awareness

        if target_awareness >= 0.7:
            self.state = RealityState.EXPANDING
            self.bounding_box = self.bounding_box.expand(1.5)

        if target_awareness >= 0.95:
            self.state = RealityState.OPEN
            self.bounding_box = self.bounding_box.expand(2.0)

        success = self.awareness_level >= 0.5
        if success and old_state != self.state:
            print(f"✓ تم كسر حاجز إدراكي: {old_state.value} → {self.state.value}")

        return success

    def reveal_hidden_layers(self) -> List[HiddenLayer]:
        """
        الكشف عن طبقات الواقع المخفية

        Returns:
            List[HiddenLayer]: قائمة الطبقات التي تم كشفها
        """
        revealed = []

        if self.perspective == PerspectiveType.OMNIDIRECTIONAL:
            for layer in self.hidden_layers:
                if not layer.is_revealed:
                    # التحقق من شروط الكشف
                    if self._check_unlock_condition(layer):
                        layer.is_revealed = True
                        layer.coordinates = {
                            'x': (self.bounding_box.max_x + self.bounding_box.min_x) / 2,
                            'y': (self.bounding_box.max_y + self.bounding_box.min_y) / 2,
                            'z': (self.bounding_box.max_z + self.bounding_box.min_z) / 2 + 100
                        }
                        revealed.append(layer)
                        print(f"🌟 تم كشف الطبقة المخفية: {layer.name}")

        return revealed

    def _check_unlock_condition(self, layer: HiddenLayer) -> bool:
        """التحقق من شرط كشف طبقة معينة"""
        condition = layer.unlock_condition

        if condition == "perspective_shift_90":
            return self.awareness_level >= 0.6
        elif condition == "temporal_loop_break":
            return self.temporal_loop.break_loop()
        elif condition == "omnidirectional_awareness":
            return self.awareness_level >= 0.95 and self.perspective == PerspectiveType.OMNIDIRECTIONAL

        return False

    def simulate_temporal_loop(self, duration: float = 5.0) -> Dict:
        """
        محاكاة الحلقة الزمنية المكررة

        Args:
            duration: مدة المحاكاة بالثواني

        Returns:
            Dict: إحصائيات الحلقة الزمنية
        """
        print("⏳ بدء محاكاة الحلقة الزمنية...")
        start = time.time()

        while time.time() - start < duration:
            pos = self.temporal_loop.get_current_position()
            progress = pos / self.temporal_loop.loop_duration

            # عرض تقدم الحلقة
            bar_length = 40
            filled = int(bar_length * progress)
            bar = '█' * filled + '░' * (bar_length - filled)

            print(f"\r[{bar}] {progress*100:.1f}% - التكرار #{self.temporal_loop.iteration_count + 1}", end='', flush=True)
            time.sleep(0.1)

        self.temporal_loop.iteration_count += 1

        # محاولة كسر الحلقة
        if self.temporal_loop.break_loop():
            print("\n\n✨ تم كسر الحلقة الزمنية!")
            self.state = RealityState.OPEN
        else:
            print(f"\n\n🔄 استمرت الحلقة الزمنية (التكرار #{self.temporal_loop.iteration_count})")

        return {
            'iterations': self.temporal_loop.iteration_count,
            'is_broken': not self.temporal_loop.is_active,
            'duration': duration
        }

    def get_reality_metrics(self) -> Dict:
        """الحصول على مقاييس الواقع الحالية"""
        return {
            'perspective': self.perspective.value,
            'state': self.state.value,
            'awareness_level': self.awareness_level,
            'bounding_volume': (
                (self.bounding_box.max_x - self.bounding_box.min_x) *
                (self.bounding_box.max_y - self.bounding_box.min_y) *
                (self.bounding_box.max_z - self.bounding_box.min_z)
            ),
            'revealed_layers': sum(1 for l in self.hidden_layers if l.is_revealed),
            'total_layers': len(self.hidden_layers),
            'temporal_loop_active': self.temporal_loop.is_active,
            'temporal_iterations': self.temporal_loop.iteration_count
        }


# دالة توضيحية للاستخدام السريع
def demo():
    """عرض توضيحي لمحرك الواقع"""
    print("=" * 60)
    print("🌌 Beyond the Facade - Reality Engine Demo")
    print("=" * 60)

    # إنشاء واقع مقيد
    reality = RealityEngine(perspective="linear", bounds="atmosphere")
    print("\n" + reality.describe())

    # توسيع الوعي تدريجياً
    print("\n🧘开始 توسيع الوعي...")
    for i in range(5):
        reality.expand_awareness(mode="gradual")
        time.sleep(0.3)

    print("\n" + reality.describe())

    # التحول إلى منظور شامل
    print("\n🔄 التحول إلى المنظور الشامل 360°...")
    reality.expand_awareness(mode="omnidirectional")

    # كشف الطبقات المخفية
    print("\n🔍 الكشف عن الطبقات المخفية...")
    revealed = reality.reveal_hidden_layers()

    print("\n" + reality.describe())

    # محاكاة الحلقة الزمنية
    print("\n⏰ محاكاة الحلقة الزمنية...")
    loop_stats = reality.simulate_temporal_loop(duration=3.0)

    print("\n📊 مقاييس الواقع النهائية:")
    metrics = reality.get_reality_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("✨ انتهى العرض التوضيحي")
    print("=" * 60)


if __name__ == "__main__":
    demo()