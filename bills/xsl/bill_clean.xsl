<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
	xmlns:xhtml="http://www.w3.org/1999/xhtml"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:mygov="http://watchingaz.us/utilities"
	exclude-result-prefixes="xhtml xsl, mygov">
	<xsl:output method="html" version="1.0" encoding="iso-8859-1" indent="yes" omit-xml-declaration="yes"/>
	<xsl:variable name="sectionTitle"></xsl:variable>
        <xsl:variable name="pClass"></xsl:variable>
        <xsl:variable name="emphasize">Insert</xsl:variable>
        
	<xsl:template match="@*|node()">
	<xsl:copy>
  		<xsl:apply-templates/>
	</xsl:copy>
	</xsl:template>
        
	<!-- Remove MsoNormal replace with grid-line -->
	<xsl:template match="node()[@class='MsoNormal']">
	    <xsl:copy>
	        <xsl:attribute name="class">grid-line</xsl:attribute>
	        <xsl:apply-templates/>
	    </xsl:copy>
	</xsl:template>
        
	<!-- Remove for some P's that are missed MsoNormal replace with grid-line -->
	<xsl:template match="p[@class='MsoNormal']">
	    <xsl:copy>
	        <xsl:attribute name="class">grid-line</xsl:attribute>
	        <xsl:apply-templates/>
	    </xsl:copy>
	</xsl:template>
	
	<xsl:template match="span[@class='TITLE']">
	    <span>
	        <xsl:attribute name="class">Title</xsl:attribute>
	        <xsl:copy-of select="child[@text()]"/>
	    </span>
	</xsl:template>
	<!-- Match the text that is being added and replace it with our class -->
	<xsl:template match="span[@class='UP']">
	    <span>
	        <xsl:attribute name="class">Insert</xsl:attribute>
	        <xsl:apply-templates/>
	    </span>
	</xsl:template>
	
	<xsl:template match="span[@style='color:blue']">
	    <xsl:value-of select="text()"/>
	</xsl:template>
	<xsl:template match="span[@style='color:red']">
	    <xsl:value-of select="text()"/>
	</xsl:template>
	
	<xsl:template match="div[@class='Section2']/p">
	    <xsl:variable name="node_id" select="mygov:getNid(.)"/>
            <xsl:choose>
                <xsl:when test="starts-with(./@class, 'P')">
                    <div>
                        <xsl:attribute name="class">billtext_container</xsl:attribute>
                        <p>
                            <xsl:attribute name="class">billtext</xsl:attribute>
			    <xsl:attribute name="nid"><xsl:value-of select="$node_id"/></xsl:attribute>
                            <xsl:apply-templates select="*|node()"/>
                        </p>
			<span class="billcomment-actions">
			{% if no_throttle %}
			{% get_comment_count for bills.versiontext '<xsl:value-of select="$node_id"/>' as node_count %}
				<xsl:text disable-output-escaping="yes">{% if node_count > 0 %}</xsl:text>
				<span><a href="#show" class="show-comments">Show Comments</a>{{ node_count }}</span>
				{% endif %}
				{% if can_comment %}
				<span><a href="/comments/" class="add-comment">Add Comment</a></span>
				{% endif %}
				{% if prefs.beta.show_statute %}
				<span><a href="/statute/" class="show-statute">Show Statute</a></span>
				{% endif %}
				{% if prefs.beta.email_section %}
				<span><a href="/share/" class="email-section">Share</a></span>
				{% endif %}
			{% endif %}
			</span>
                        <div class="HControl">
			{% if no_throttle %}
				<xsl:text disable-output-escaping="yes">{% if node_count > 0 %}</xsl:text>
				<div class="comment-list">
				{% get_comment_list for bills.versiontext '<xsl:value-of select="$node_id"/>' as node_comments %}
				{% for comment in node_comments %}
				<div class="comment {{{{comment.object_pk}}}}">
				    <xsl:variable name="cid">{{comment.id}}</xsl:variable>
				    <a>
					<xsl:attribute name="name"><xsl:value-of select="$cid"/></xsl:attribute>
				    </a>
				    <a href="{{% get_comment_permalink comment %}}">
				    permalink for comment #{{ forloop.counter }}
				    </a>
				    <div>
				    {{ comment.comment }}
				    </div>
				</div>
				{% endfor %}
				</div>
				{% endif %}
			{% endif %}
                        </div>
                    </div>
                </xsl:when>
                <xsl:when test="starts-with(./@class, 'SEC')">
                    <p>
                        <xsl:attribute name="class">sec-head</xsl:attribute>
                        <xsl:variable name="sec_id" select="./span[@class='SNUM']/span[@style='color:green']/text()"/>
			<xsl:attribute name="nid"><xsl:value-of select="$node_id"/></xsl:attribute>
                        <xsl:choose>
                        <xsl:when test="contains($sec_id, '.')">
                            <xsl:attribute name="id"><xsl:value-of select="substring-before($sec_id, '.')"/></xsl:attribute>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:attribute name="id"><xsl:value-of select="$sec_id"/></xsl:attribute>
                        </xsl:otherwise>
                        </xsl:choose>
                        <xsl:apply-templates select="*|node()"/>
                    </p>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:copy>
                        <xsl:apply-templates select="@*|node()"/>
                    </xsl:copy>
                </xsl:otherwise>
            </xsl:choose>
	</xsl:template>
	<xsl:template match="span[@class='O']">
	    <span>
	        <xsl:attribute name="class">strike</xsl:attribute>
	        <xsl:apply-templates/>
	    </span>
	</xsl:template>
	<xsl:template match="span[@class='SNUM']">
	    <a>
	        <xsl:variable name="sec_id" select="./span[@style='color:green']/text()"/>
	        <xsl:choose>
	        <xsl:when test="contains($sec_id, '.')">
	            <xsl:attribute name="href"><xsl:value-of select="substring-before($sec_id, '.')"/></xsl:attribute>
	        </xsl:when>
	        <xsl:otherwise>
	            <xsl:attribute name="href"><xsl:value-of select="$sec_id"/></xsl:attribute>
	        </xsl:otherwise>
	        </xsl:choose>
	        <xsl:attribute name="class">statute-link</xsl:attribute>
	        <xsl:attribute name="rel">no-follow</xsl:attribute>
  		<xsl:value-of select="./span[@style='color:green']/text()"/>
	    </a>
	</xsl:template>
	<xsl:template match="@*|node()">
            <xsl:copy>
                <xsl:apply-templates select="@*|node()"/>
            </xsl:copy>
	</xsl:template>
	
</xsl:stylesheet>
