-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 06 Ara 2020, 16:36:25
-- Sunucu sürümü: 10.4.13-MariaDB
-- PHP Sürümü: 7.4.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `mydatabase`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `articles`
--

CREATE TABLE `articles` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `author` text NOT NULL,
  `content` text NOT NULL,
  `created_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `articles`
--

INSERT INTO `articles` (`id`, `title`, `author`, `content`, `created_date`) VALUES
(4, 'Demo 102', 'samil_y', '<p>Mustafa Kemal Atat&uuml;rk 1881 yılında Sel&acirc;nik&#39;te Kocakasım Mahallesi, Isl&acirc;hh&acirc;ne Caddesi&#39;ndeki &uuml;&ccedil; katlı pembe evde doğdu. Babası Ali Rıza Efendi, annesi Z&uuml;beyde Hanım&#39;dır. Baba tarafından dedesi Hafız Ahmet Efendi XIV-XV. y&uuml;zyıllarda Konya ve Aydın&#39;dan Makedonya&#39;ya yerleştirilmiş Kocacık Y&ouml;r&uuml;klerindendir. Annesi Z&uuml;beyde Hanım ise&nbsp; Sel&acirc;nik yakınlarındaki Langaza kasabasına yerleşmiş eski bir T&uuml;rk ailesinin kızıdır. Milis subaylığı, evkaf katipliği ve kereste ticareti yapan Ali Rıza Efendi, 1871 yılında Z&uuml;beyde Hanım&#39;la evlendi. Atat&uuml;rk&#39;&uuml;n beş kardeşinden d&ouml;rd&uuml; k&uuml;&ccedil;&uuml;k yaşlarda &ouml;ld&uuml;, sadece Makbule (Atadan) 1956 yılına değin yaşadı.</p>\r\n', '2020-09-24 12:27:32'),
(9, 'Demo 101', 'samil_y', '<p>asdas</p>\r\n', '2020-12-06 15:22:03');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`) VALUES
(2, 'Alp Aslan', 'alp@gmail.com', 'alpaslan', '$5$rounds=535000$QblGvBvVsrgQ8Op3$BWFNMQWXoIvTzKcGx1Uc7.X.q1pU3ND3jflNynIm.U5'),
(4, 'Doğan ', 'dgn@gmail.com', 'dogan', '$5$rounds=535000$JMrXYXPNbzcsVrTN$cnHdzQRVUn3C9jEtdmEm0vmyqWz54ext0QPsrivEMX0'),
(5, 'Oguz Atay', 'oguz@gmail.com', 'tutunmadı', '$5$rounds=535000$HpCn8rD40EiLtFz/$8T6IV8GjzAFxN54bgBuhTEF/FLosgJoS2HXnEk7iOAC'),
(6, 'Şamil ', 'samil@gmail.com', 'samil_y', '$5$rounds=535000$Z3spiAFkHeRoZcBG$RtwsrbI4QE123ArfGJqA/gxWn07c99HzHzUMbc.kBc.');

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Tablo için AUTO_INCREMENT değeri `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
