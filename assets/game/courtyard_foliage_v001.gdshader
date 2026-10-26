shader_type spatial;
render_mode cull_disabled;
uniform vec4 tint : source_color = vec4(.20,.28,.09,1.0);
uniform float wind_strength=.035;
void vertex() {
	vec3 p=(MODEL_MATRIX*vec4(VERTEX,1.0)).xyz;
	float weight=clamp(VERTEX.y,0.0,1.0);
	VERTEX.x+=sin(TIME*.85+p.x*.9+p.z*.61)*wind_strength*weight;
	VERTEX.z+=sin(TIME*.61+p.z*.8)*wind_strength*.55*weight;
}
void fragment() {
	ALBEDO=tint.rgb*COLOR.rgb*.72;
	ROUGHNESS=.88;
	BACKLIGHT=ALBEDO*.18;
}
