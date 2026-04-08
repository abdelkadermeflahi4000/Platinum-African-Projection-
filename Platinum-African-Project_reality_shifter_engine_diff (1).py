--- Platinum-African-Project/reality_shifter/engine.py (原始)


+++ Platinum-African-Project/reality_shifter/engine.py (修改后)
"""
🌀 Platinum African Project - Reality Shifter Engine
محرك الانتقال بين العوالم

This module implements the reality shifting mechanism that enables
transition between "Platinum" (current reality) and "Other Lands".
"""

import numpy as np
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class RealityState(Enum):
    """حالات الواقع الممكنة"""
    PLATINUM = "platinum"              # الواقع الحالي (بلاتينية)
    OTHER_LANDS = "other_lands"        # الأراضي الأخرى
    LIMINAL = "liminal"                # الحالة الحدية (بين العالمين)
    COLLAPSED = "collapsed"            # واقع منهيار
    TRANSCENDENT = "transcendent"      # واقع متسامٍ


@dataclass
class DimensionalCoordinates:
    """إحداثيات بُعدية للواقع"""
    spatial_x: float
    spatial_y: float
    spatial_z: float
    temporal_w: float       # البعد الزمني الإضافي
    consciousness_v: float  # بعد الوعي
    ancestral_connection: float  # الاتصال بالأجداد
    entropy_level: float    # مستوى الإنتروبيا

    def to_dict(self) -> Dict:
        return {
            'spatial_x': self.spatial_x,
            'spatial_y': self.spatial_y,
            'spatial_z': self.spatial_z,
            'temporal_w': self.temporal_w,
            'consciousness_v': self.consciousness_v,
            'ancestral_connection': self.ancestral_connection,
            'entropy_level': self.entropy_level
        }


@dataclass
class ShiftResult:
    """نتيجة عملية الانتقال"""
    success: bool
    from_state: RealityState
    to_state: RealityState
    coherence_achieved: float
    coordinates: DimensionalCoordinates
    duration_ms: float
    warnings: List[str]
    message: str


class RealityShifter:
    """
    محرك الانتقال الواقعي

    يُمكّن الانتقال الآمن بين حالات الواقع المختلفة
    باستخدام خوارزميات مستوحاة من الفيزياء النظرية
    والتقاليد الأفريقية القديمة
    """

    def __init__(self, safety_threshold: float = 0.85):
        """
        تهيئة محرك الانتقال

        Args:
            safety_threshold: عتبة السلامة الدنيا للانتقال
        """
        self.safety_threshold = safety_threshold
        self.current_state = RealityState.PLATINUM
        self.shift_history: List[ShiftResult] = []
        self.dimension_map: Dict[str, DimensionalCoordinates] = {}

        # معاملات النظام
        self.max_entropy = 3.5  # الحد الأقصى للإنتروبيا المسموح بها
        self.min_coherence = 0.70  # الحد الأدنى للتماسك

        print(f"🌀 محرك الانتقال الواقعي مُهيأ (عتبة السلامة: {safety_threshold})")

    def generate_platinum_coordinates(self) -> DimensionalCoordinates:
        """
        توليد إحداثيات واقع بلاتينية الحالي

        Returns:
            إحداثيات الواقع الحالي
        """
        return DimensionalCoordinates(
            spatial_x=np.random.uniform(-100, 100),
            spatial_y=np.random.uniform(-100, 100),
            spatial_z=np.random.uniform(-100, 100),
            temporal_w=time.time(),
            consciousness_v=np.random.uniform(0.4, 0.7),  # وعي محدود في الواقع الحالي
            ancestral_connection=np.random.uniform(0.3, 0.6),  # اتصال ضعيف بالأجداد
            entropy_level=np.random.uniform(1.5, 2.5)  # إنتروبيا متوسطة
        )

    def generate_other_lands_coordinates(self,
                                         consciousness_level: float) -> DimensionalCoordinates:
        """
        توليد إحداثيات الأراضي الأخرى

        Args:
            consciousness_level: مستوى الوعي المطلوب

        Returns:
            إحداثيات الأراضي الأخرى
        """
        # الأراضي الأخرى لها خصائص مختلفة جذرياً
        return DimensionalCoordinates(
            spatial_x=np.random.uniform(-1000, 1000),
            spatial_y=np.random.uniform(-1000, 1000),
            spatial_z=np.random.uniform(-1000, 1000),
            temporal_w=np.random.uniform(0, 10),  # زمن غير خطي
            consciousness_v=min(1.0, consciousness_level * 1.3),  # وعي موسع
            ancestral_connection=min(1.0, consciousness_level * 1.5),  # اتصال قوي بالأجداد
            entropy_level=np.random.uniform(0.5, 1.5)  # إنتروبيا منخفضة (نظام أعلى)
        )

    def calculate_coherence(self,
                           hrv_signal: np.ndarray,
                           eeg_signal: np.ndarray) -> float:
        """
        حساب التماسك الحيوي الشامل

        Args:
            hrv_signal: إشارة HRV
            eeg_signal: إشارة EEG

        Returns:
            درجة التماسك (0-1)
        """
        # تماسك HRV
        hrv_mean = np.mean(hrv_signal)
        hrv_std = np.std(hrv_signal)
        hrv_coherence = 1.0 / (1.0 + abs(hrv_std / max(abs(hrv_mean), 0.1)))

        # تماسك EEG (نسبة Alpha/Theta)
        if len(eeg_signal) > 100:
            fft = np.fft.fft(eeg_signal)
            freqs = np.fft.fftfreq(len(eeg_signal))

            alpha_power = np.sum(np.abs(fft[(freqs >= 8) & (freqs <= 13)]) ** 2)
            theta_power = np.sum(np.abs(fft[(freqs >= 4) & (freqs <= 8)]) ** 2)

            eeg_coherence = min(1.0, alpha_power / max(theta_power, 0.1))
        else:
            eeg_coherence = 0.5

        # تماسك شامل مرجح
        overall = (hrv_coherence * 0.5 + eeg_coherence * 0.5)

        return min(max(overall, 0.0), 1.0)

    def calculate_entropy(self, signal: np.ndarray) -> float:
        """
        حساب الإنتروبيا الطيفية للإشارة

        Args:
            signal: الإشارة الحيوية

        Returns:
            قيمة الإنتروبيا
        """
        # تحويل فورييه
        fft = np.fft.fft(signal)
        power_spectrum = np.abs(fft) ** 2

        # تطبيع لتوزيع احتمالي
        prob_dist = power_spectrum / np.sum(power_spectrum)
        prob_dist = prob_dist[prob_dist > 0]  # تجنب اللوغاريتم của الصفر

        # إنتروبيا شانون
        entropy = -np.sum(prob_dist * np.log2(prob_dist))

        return entropy

    def attempt_shift(self,
                     hrv_signal: np.ndarray,
                     eeg_signal: np.ndarray,
                     intention: str = "exploration") -> ShiftResult:
        """
        محاولة الانتقال إلى الأراضي الأخرى

        Args:
            hrv_signal: إشارة HRV للمشارك
            eeg_signal: إشارة EEG للمشارك
            intention: نية الانتقال

        Returns:
            ShiftResult تحتوي على نتيجة المحاولة
        """
        start_time = time.perf_counter()
        warnings = []

        print("\n" + "=" * 70)
        print("🌀 بدء بروتوكول الانتقال الواقعي...")
        print("=" * 70)

        # حساب المقاييس الحيوية
        coherence = self.calculate_coherence(hrv_signal, eeg_signal)
        entropy = self.calculate_entropy(np.concatenate([hrv_signal, eeg_signal]))

        print(f"\n📊 التحليل الحيوي:")
        print(f"   التماسك: {coherence:.4f}")
        print(f"   الإنتروبيا: {entropy:.4f}")
        print(f"   النية: {intention}")

        # فحص شروط السلامة
        if coherence < self.min_coherence:
            warnings.append(f"التماسك منخفض ({coherence:.3f} < {self.min_coherence})")

        if entropy > self.max_entropy:
            warnings.append(f"الإنتروبيا مرتفعة ({entropy:.3f} > {self.max_entropy})")

        # تحديد النجاح أو الفشل
        success = (coherence >= self.safety_threshold and
                  entropy <= self.max_entropy and
                  len(warnings) == 0)

        if success:
            # انتقال ناجح!
            target_state = RealityState.OTHER_LANDS
            coordinates = self.generate_other_lands_coordinates(coherence)

            print(f"\n✅ شروط الانتقال محققة!")
            print(f"   التماسك كافٍ: {coherence:.4f} >= {self.safety_threshold}")
            print(f"   الإنتروبيا مقبولة: {entropy:.4f} <= {self.max_entropy}")

            message = f"انتقال ناجح إلى الأراضي الأخرى بنية '{intention}'"
        else:
            # فشل الانتقال
            target_state = RealityState.PLATINUM
            coordinates = self.generate_platinum_coordinates()

            print(f"\n❌ شروط الانتقال غير محققة:")
            for warning in warnings:
                print(f"   ⚠️ {warning}")

            message = "فشل الانتقال - يرجى زيادة التماسك وخفض الإنتروبيا"

        # حساب المدة
        duration_ms = (time.perf_counter() - start_time) * 1000

        # إنشاء النتيجة
        result = ShiftResult(
            success=success,
            from_state=self.current_state,
            to_state=target_state if success else self.current_state,
            coherence_achieved=coherence,
            coordinates=coordinates,
            duration_ms=duration_ms,
            warnings=warnings,
            message=message
        )

        # تحديث الحالة الحالية
        if success:
            self.current_state = target_state

        # تسجيل في التاريخ
        self.shift_history.append(result)

        # عرض الإحداثيات
        print(f"\n🗺️ الإحداثيات البُعدية:")
        coords_dict = coordinates.to_dict()
        for dim, value in coords_dict.items():
            print(f"   {dim:20s}: {value:.4f}")

        print(f"\n⏱️ مدة العملية: {duration_ms:.3f}ms")
        print(f"\n💬 الرسالة: {message}")
        print("=" * 70)

        return result

    def emergency_rollback(self) -> ShiftResult:
        """
        تراجع طارئ إلى الواقع الحالي

        Returns:
            ShiftResult للتراجع
        """
        print("\n" + "=" * 70)
        print("🛑 تفعيل بروتوكول التراجع الطارئ...")
        print("=" * 70)

        start_time = time.perf_counter()

        # العودة إلى بلاتينية
        coordinates = self.generate_platinum_coordinates()

        duration_ms = (time.perf_counter() - start_time) * 1000

        result = ShiftResult(
            success=True,
            from_state=self.current_state,
            to_state=RealityState.PLATINUM,
            coherence_achieved=0.0,
            coordinates=coordinates,
            duration_ms=duration_ms,
            warnings=["Emergency rollback activated"],
            message="تم التراجع الطارئ بنجاح إلى الواقع الحالي"
        )

        self.current_state = RealityState.PLATINUM
        self.shift_history.append(result)

        print(f"✅ تم التراجع بنجاح خلال {duration_ms:.3f}ms")
        print("📍 العودة إلى إحداثيات بلاتينية")
        print("=" * 70)

        return result

    def get_shift_statistics(self) -> Dict:
        """
        الحصول على إحصائيات الانتقالات

        Returns:
            قاموس بالإحصائيات
        """
        if not self.shift_history:
            return {
                'total_shifts': 0,
                'successful_shifts': 0,
                'failed_shifts': 0,
                'success_rate': 0.0,
                'average_coherence': 0.0,
                'average_duration_ms': 0.0,
                'current_state': self.current_state.value
            }

        successful = [s for s in self.shift_history if s.success]

        return {
            'total_shifts': len(self.shift_history),
            'successful_shifts': len(successful),
            'failed_shifts': len(self.shift_history) - len(successful),
            'success_rate': len(successful) / len(self.shift_history),
            'average_coherence': np.mean([s.coherence_achieved for s in self.shift_history]),
            'average_duration_ms': np.mean([s.duration_ms for s in self.shift_history]),
            'current_state': self.current_state.value
        }


class RealityShiftingSystem:
    """
    نظام الانتقال الواقعي المتكامل

    يجمع بين محرك الانتقال ومحاكاة الإشارات الحيوية
    """

    def __init__(self):
        self.shifter = RealityShifter(safety_threshold=0.85)
        self.session_count = 0

    def simulate_biosignals(self,
                           coherence_target: float = 0.85,
                           duration_sec: float = 60.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        محاكاة إشارات حيوية بمستوى تماسك مستهدف

        Args:
            coherence_target: مستوى التماسك المطلوب
            duration_sec: مدة المحاكاة

        Returns:
            (hrv_signal, eeg_signal)
        """
        sample_rate = 1000
        n_samples = int(duration_sec * sample_rate)
        t = np.linspace(0, duration_sec, n_samples)

        # HRV محاكي
        noise_level = (1 - coherence_target) * 0.5
        hrv = (np.sin(2 * np.pi * 0.1 * t) * coherence_target +
               np.random.randn(n_samples) * noise_level)

        # EEG محاكي (حالة تأملية)
        alpha = np.sin(2 * np.pi * 10 * t) * coherence_target
        theta = np.sin(2 * np.pi * 6 * t) * (1 - coherence_target)
        eeg = alpha + theta + np.random.randn(n_samples) * noise_level * 0.3

        return hrv, eeg

    def full_session(self,
                    brain_state: str = "meditative",
                    intention: str = "exploration") -> ShiftResult:
        """
        جلسة انتقال واقعي كاملة

        Args:
            brain_state: حالة الدماغ المطلوبة
            intention: نية الانتقال

        Returns:
            نتيجة الجلسة
        """
        self.session_count += 1

        print("\n" + "🌟" * 35)
        print(f"   جلسة الانتقال #{self.session_count}")
        print(f"   الحالة: {brain_state} | النية: {intention}")
        print("🌟" * 35)

        # تحديد مستوى التماسك المستهدف بناءً على حالة الدماغ
        coherence_targets = {
            "meditative": 0.90,
            "focused": 0.85,
            "relaxed": 0.80,
            "stressed": 0.60
        }
        target_coherence = coherence_targets.get(brain_state, 0.75)

        # محاكاة الإشارات
        print("\n📡 توليد الإشارات الحيوية...")
        hrv, eeg = self.simulate_biosignals(
            coherence_target=target_coherence,
            duration_sec=30.0
        )
        print(f"   ✓ HRV: {len(hrv)} عينة")
        print(f"   ✓ EEG: {len(eeg)} عينة")

        # محاولة الانتقال
        result = self.shifter.attempt_shift(hrv, eeg, intention)

        return result

    def training_mode(self, sessions: int = 5) -> List[ShiftResult]:
        """
        وضع التدريب: محاولات متعددة لتحسين التماسك

        Args:
            sessions: عدد جلسات التدريب

        Returns:
            قائمة بنتائج الجلسات
        """
        print("\n" + "=" * 70)
        print(f"🎯 وضع التدريب: {sessions} جلسات")
        print("=" * 70)

        results = []

        for i in range(sessions):
            print(f"\n{'='*70}")
            print(f"جلسة تدريب #{i+1}/{sessions}")
            print('='*70)

            # زيادة التماسك تدريجياً
            target = min(0.95, 0.70 + i * 0.05)

            result = self.full_session(
                brain_state="meditative",
                intention=f"training_session_{i+1}"
            )

            results.append(result)

            #_pause بسيط
            time.sleep(0.1)

        # عرض ملخص التدريب
        print("\n" + "=" * 70)
        print("📊 ملخص التدريب:")
        stats = self.shifter.get_shift_statistics()
        print(f"   إجمالي الجلسات: {stats['total_shifts']}")
        print(f"   النجاحات: {stats['successful_shifts']}")
        print(f"   معدل النجاح: {stats['success_rate']:.2%}")
        print(f"   متوسط التماسك: {stats['average_coherence']:.4f}")
        print("=" * 70)

        return results


# === تجربة توضيحية ===
if __name__ == "__main__":
    print("=" * 70)
    print("🌀 Platinum African Project - Reality Shifter Engine")
    print("   محرك الانتقال بين العوالم - مشروع بلاتينيوم أفريقي")
    print("=" * 70)

    # تهيئة النظام
    shifting_system = RealityShiftingSystem()

    # جلسة 1: حالة متألمة (تماسك عالي)
    print("\n" + "=" * 70)
    print("جلسة 1: حالة تأملية عميقة")
    print("=" * 70)
    result1 = shifting_system.full_session(
        brain_state="meditative",
        intention="ancestral_connection"
    )

    # جلسة 2: حالة مركزة
    print("\n" + "=" * 70)
    print("جلسة 2: حالة تركيز")
    print("=" * 70)
    result2 = shifting_system.full_session(
        brain_state="focused",
        intention="knowledge_seeking"
    )

    # جلسة 3: حالة متوترة (تماسك منخفض)
    print("\n" + "=" * 70)
    print("جلسة 3: حالة توتر")
    print("=" * 70)
    result3 = shifting_system.full_session(
        brain_state="stressed",
        intention="escape"
    )

    # عرض الإحصائيات النهائية
    print("\n" + "=" * 70)
    print("📊 الإحصائيات النهائية:")
    print("=" * 70)
    stats = shifting_system.shifter.get_shift_statistics()

    for key, value in stats.items():
        if isinstance(value, float):
            print(f"   {key:25s}: {value:.4f}")
        else:
            print(f"   {key:25s}: {value}")

    # اختبار التراجع الطارئ
    print("\n" + "=" * 70)
    print("اختبار التراجع الطارئ")
    print("=" * 70)
    rollback_result = shifting_system.shifter.emergency_rollback()
    print(f"نتيجة التراجع: {rollback_result.message}")

    print("\n" + "=" * 70)
    print("✨ اكتملت تجربة محرك الانتقال بنجاح!")
    print("=" * 70)