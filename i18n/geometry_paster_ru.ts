<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="ru">
<context>
    <name>AboutDialogBase</name>
    <message>
        <location filename="../about_dialog_base.ui" line="14"/>
        <source>About {plugin_name}</source>
        <translation>О {plugin_name}</translation>
    </message>
    <message>
        <location filename="../about_dialog_base.ui" line="27"/>
        <source>&lt;p align=&quot;center&quot;&gt;{plugin_name}&lt;/p&gt;</source>
        <translation>&lt;p align=&quot;center&quot;&gt;{plugin_name}&lt;/p&gt;</translation>
    </message>
    <message>
        <location filename="../about_dialog_base.ui" line="40"/>
        <source>&lt;p&gt;{description}&lt;/p&gt;
&lt;p&gt;{about}&lt;/p&gt;
&lt;p&gt;&lt;b&gt;Developers:&lt;/b&gt; &lt;a href=&quot;{main_url}/{utm}&quot;&gt;{authors}&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;&lt;b&gt;Homepage:&lt;/b&gt; &lt;a href=&quot;{homepage_url}&quot;&gt;{homepage_url}&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;&lt;b&gt;Video with an overview of the plugin:&lt;/b&gt; &lt;a href=&quot;{video_url}&quot;&gt;
{video_url}&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;&lt;b&gt;Please report bugs at&lt;/b&gt; &lt;a href=&quot;{tracker_url}&quot;&gt;bugtracker&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;Other helpful services by NextGIS:
&lt;ul&gt;&lt;li&gt;&lt;b&gt;Convenient up-to-date data extracts for any place in the world:
&lt;a href=&quot;{main_url}/{utm}&quot;&gt;{main_url}&lt;/a&gt;&lt;/b&gt;&lt;/li&gt;
&lt;li&gt;&lt;b&gt;Fully featured Web GIS service:
&lt;a href=&quot;{main_url}/pricing-base{utm}&quot;&gt;
{main_url}/pricing-base&lt;/a&gt;&lt;/b&gt;&lt;/li&gt;&lt;/ul&gt;
&lt;/p&gt;</source>
        <translation>&lt;p&gt;{description}&lt;/p&gt;
&lt;p&gt;{about}&lt;/p&gt;
&lt;p&gt;&lt;b&gt;Разработчики:&lt;/b&gt; &lt;a href=&quot;{main_url}&quot;&gt;{authors}&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;&lt;b&gt;Домашняя страница:&lt;/b&gt; &lt;a href=&quot;{homepage_url}&quot;&gt;{homepage_url}&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;&lt;b&gt;Видео с обзором плагина:&lt;/b&gt; &lt;a href=&quot;{video_url}&quot;&gt;
{video_url}&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;&lt;b&gt;Пожалуйста, сообщайте о багах в&lt;/b&gt; &lt;a href=&quot;{tracker_url}&quot;&gt;багтрекер&lt;/a&gt;&lt;/p&gt;
&lt;p&gt;Другие полезные сервисы NextGIS:
&lt;ul&gt;&lt;li&gt;&lt;b&gt;Удобная выборка актуальных данных из любой точки мира:
&lt;a href=&quot;{main_url}/{utm}&quot;&gt;{main_url}&lt;/a&gt;&lt;/b&gt;&lt;/li&gt;
&lt;li&gt;&lt;b&gt;Полнофункциональный веб-ГИС-сервис:
&lt;a href=&quot;{main_url}/pricing-base{utm}&quot;&gt;
{main_url}/pricing-base{&lt;/a&gt;&lt;/b&gt;&lt;/li&gt;&lt;/ul&gt;
&lt;/p&gt;</translation>
    </message>
</context>
<context>
    <name>Plugin</name>
    <message>
        <location filename="../plugin.py" line="255"/>
        <source>Paste Geometry</source>
        <translation>Вставить геометрию</translation>
    </message>
    <message>
        <location filename="../plugin.py" line="196"/>
        <source>Paste geometry</source>
        <translation>Вставить геометрию</translation>
    </message>
    <message>
        <location filename="../plugin.py" line="144"/>
        <source>Fail to paste. Multiple features in the clipboard.</source>
        <translation>Ошибка вставки. В буфере несколько объектов.</translation>
    </message>
    <message>
        <location filename="../plugin.py" line="151"/>
        <source>Nothing to paste. No features in the clipboard.</source>
        <translation>Нечего вставлять. Буфер пуст.</translation>
    </message>
    <message>
        <location filename="../plugin.py" line="164"/>
        <source>Multiple features are selected. There should be only one.</source>
        <translation>Выбрано несколько объектов, но нужен только один.</translation>
    </message>
    <message>
        <location filename="../plugin.py" line="173"/>
        <source>Nowhere to paste. No target feature selected.</source>
        <translation>Некуда вставлять. Не выбран ни один объект.</translation>
    </message>
    <message>
        <location filename="../plugin.py" line="183"/>
        <source>Incompatible geometries. Trying to paste %s to %s</source>
        <translation>Несовместимые геометрии. Попытка вставки %s в %s</translation>
    </message>
    <message>
        <location filename="../plugin.py" line="196"/>
        <source>Something is wrong. Can&apos;t change geometry.</source>
        <translation>Что-то пошло не так. Не удалось изменить геометрию.</translation>
    </message>
    <message>
        <location filename="../plugin.py" line="240"/>
        <source>Select a target feature!</source>
        <translation>Выберите целевой объект!</translation>
    </message>
    <message>
        <location filename="../plugin.py" line="243"/>
        <source>Start editing a vector layer!</source>
        <translation>Начните редактировать целевой слой!</translation>
    </message>
    <message>
        <location filename="../plugin.py" line="248"/>
        <source>Copy feature with the geometry you need to paste first!</source>
        <translation>Сначала скопируйте объект с геометрией которую нужно вставить!</translation>
    </message>
    <message>
        <location filename="../plugin.py" line="121"/>
        <source>Geometry Paster</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../plugin.py" line="100"/>
        <source>About plugin…</source>
        <translation>О плагине…</translation>
    </message>
</context>
</TS>
